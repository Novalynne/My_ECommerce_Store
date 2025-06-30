import random
from django.shortcuts import render, get_object_or_404
from products.models import Product, ProductStock, Size
from .forms import AddToCartForm, ReturnRequestForm
from django.views.generic import ListView
from decimal import Decimal
from django.shortcuts import redirect
from django.contrib import messages
from .models import Cart, Order, OrderProduct, Profile, Status, ReturnRequest
from django.db import transaction
from django.utils import timezone

# Create your views here.

# --- CART VIEWS ---
# CartSummary, add_to_cart, remove_from_cart, update_cart

class CartSummary(ListView):
    model = Cart
    template_name = 'cart_summary.html'
    paginate_by = 10
    context_object_name = 'cart_products'

    def get_cart_products_and_total(self):
        user = self.request.user
        cart_products = Cart.objects.filter(user__user=user)

        total = 0
        cart_with_stock = []
        for item in cart_products:
            price = item.product.sale_price if item.product.is_sale else item.product.price
            total += price * item.quantity

            product_stock = ProductStock.objects.filter(product=item.product, size=item.size).first()
            stock_available = product_stock.stock if product_stock else 0

            cart_with_stock.append({
                'item': item,
                'stock_available': stock_available
            })

        return cart_with_stock, total

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart_products, total = self.get_cart_products_and_total()
        context['cart_products'] = cart_products
        context['total'] = total
        return context

    def post(self, request, *args, **kwargs):
        cart_products, total = self.get_cart_products_and_total()
        if not cart_products:
            messages.warning(request, "Your cart is empty.")
            return redirect('cart_summary')

        # Controllo stock
        for cart_item in cart_products:
            item = cart_item['item']
            stock_available = cart_item['stock_available']

            if stock_available <= 0:
                messages.warning(request, f"No stock available for {item.product.name} in size {item.size.name}.")
                return redirect('cart_summary')

            if stock_available < item.quantity:
                messages.warning(request, f"Not enough stock for {item.product.name} in size {item.size.name}. Available: {stock_available}, Requested: {item.quantity}")
                return redirect('cart_summary')

        context = {
            'cart_products': cart_products,
            'total': total,
        }
        return render(request, 'payment.html', context)

def add_to_cart(request):
    if request.method == "POST":
        form = AddToCartForm(request.POST)
        if form.is_valid():
            product_id = request.POST.get("product_id")
            size = form.cleaned_data["size"]
            quantity = form.cleaned_data["quantity"]
            product = get_object_or_404(Product, pk=product_id)
            stock = get_object_or_404(ProductStock, product=product, size=size)
            if quantity > stock.stock:
                messages.warning(request, "Quantity of item not available.")
                return redirect("product", pk=product_id)
            # Salva nel carrello
            profile = Profile.objects.get(user=request.user)
            cart_item, created = Cart.objects.get_or_create(
                user=profile, product=product, size=size,
                defaults={"quantity": quantity}
            )
            if not created:
                cart_item.quantity += quantity
                cart_item.save()
            messages.success(request, "Item added to your cart!")
            return redirect("product", pk=product_id)
        else:
            messages.warning(request, "Data not valid.")
            return redirect(request.META.get("HTTP_REFERER", "/"))
    return redirect("homepage")

def remove_from_cart(request):
    if request.method == "POST":
        product_id = request.POST.get("product_id")
        size_name = request.POST.get("size_name")
        profile = Profile.objects.get(user=request.user)
        product = get_object_or_404(Product, pk=product_id)
        size = get_object_or_404(Size, name=size_name)
        cart_item = Cart.objects.filter(user=profile, product=product, size=size).first()
        if cart_item:
            cart_item.delete()
        else:
            return redirect("cart_summary")
    return redirect("cart_summary")
def update_cart(request):
    if request.method == "POST":
        product_id = request.POST.get("product_id")
        size_name = request.POST.get("size_name")
        action = request.POST.get("action")
        profile = Profile.objects.get(user=request.user)
        product = get_object_or_404(Product, pk=product_id)
        size = get_object_or_404(Size, name=size_name)
        cart_item = Cart.objects.filter(user=profile, product=product, size=size).first()
        if cart_item:
            if action == "increase":
                stock = ProductStock.objects.get(product=product, size=size)
                if cart_item.quantity < stock.stock:
                    cart_item.quantity += 1
                    cart_item.save()
                else:
                    messages.warning(request, "Cannot increase quantity beyond available stock.")
            elif action == "decrease":
                if cart_item.quantity > 1:
                    cart_item.quantity -= 1
                    cart_item.save()
                else:
                    cart_item.delete()
    return redirect("cart_summary")

# --- WISHLIST VIEWS ---
# wishlist, toggle_wishlist

class wishlist(ListView):
    model = Product
    template_name = 'wishlist.html'
    paginate_by = 10
    context_object_name = 'wishlist_items'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        profile = Profile.objects.get(user=user)
        wishlist = profile.favourites.all()
        context['wishlist_items'] = wishlist
        return context

def toggle_wishlist(request, product_id):
    user = request.user
    profile = Profile.objects.get(user=user)
    product = get_object_or_404(Product, pk=product_id)

    if request.method == "POST":
        if product not in profile.favourites.all():
            profile.favourites.add(product)
        else:
            profile.favourites.remove(product)

        # Redirect alla pagina precedente, con fallback alla homepage
        referer = request.META.get('HTTP_REFERER')
        if referer:
            return redirect(referer)
    return redirect('homepage')

# --- ORDER VIEWS ---
# place_order, 0rderSummary, cancel_order, order_change_status, ManagerOrderList, order_return, submit_return_request, return_requests_for_order

def place_order(request):
    user = request.user
    profile = Profile.objects.get(user=user)
    cart_items = Cart.objects.filter(user=profile)

    if request.method == "POST":
        money = Decimal(random.randint(1000, 20000)) / 100  # Simulazione fondi disponibili (tra 10.00€ e 200.00€)
        total = Decimal(request.POST.get("total", "0.00"))

        if total > money:
            messages.warning(request, "Insufficient funds to place the order.")
            print(f"Total: {total}, Money: {money}")
            return redirect("cart_summary")

        try:
            with transaction.atomic():
                order = Order.objects.create(
                    user=profile,
                    address=profile.address,
                    user_email=profile.user.email,
                    total=total,
                    status_id=1
                )

                order_products = []

                for item in cart_items:
                    product_stock = ProductStock.objects.filter(product=item.product, size=item.size).first()

                    if not product_stock:
                        raise ValueError(f"No stock available for {item.product.name} in size {item.size.name}.")

                    if product_stock.stock < item.quantity:
                        raise ValueError(f"Not enough stock for {item.product.name} in size {item.size.name}. Available: {product_stock.stock}, Requested: {item.quantity}")

                    # Stock sufficiente, scala
                    product_stock.stock -= item.quantity
                    product_stock.save()
                    if product_stock.stock <= 0:
                        product_stock.delete()

                    order_product = OrderProduct(
                        order=order,
                        product=item.product,
                        product_name=item.product.name,
                        quantity=item.quantity,
                        size=item.size,
                        unit_price=item.product.price if not item.product.is_sale else item.product.sale_price
                    )
                    order_products.append(order_product)

                OrderProduct.objects.bulk_create(order_products)
                cart_items.delete()

        except ValueError as e:
            messages.warning(request, str(e))
            return redirect("cart_summary")

        return redirect("order_summary")

    return redirect("cart_summary")


class OrderSummery(ListView):
    model = Order
    template_name = 'order_summary.html'
    context_object_name = 'orders'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        orders = Order.objects.filter(user__user=user).order_by('-date')

        for order in orders:
            order.update_status()
            order.non_refundable()

        context['orders'] = orders
        return context

def cancel_order(request, order_id):
    user = request.user
    order = get_object_or_404(Order, id=order_id, user__user=user)

    if order.status.id != 1:  # 1 = "IN THE MAKING" , it is just a double check it shoud never occour for the order to not be in the making
        messages.warning(request, "Order isn't in the making.")
        return redirect("order_summary")

    try:
        with transaction.atomic():
            order_products = OrderProduct.objects.filter(order=order)

            for op in order_products:
                product_stock, created = ProductStock.objects.get_or_create(
                    product=op.product,
                    size=op.size,
                    defaults={"stock": 0}
                )
                product_stock.stock += op.quantity
                product_stock.save()

            order.delete()
            messages.success(request, "Order successfully cancelled and stock restored.")
    except Exception as e:
        messages.warning(request, f"Error while cancelling the order: {str(e)}")
    return redirect("order_summary")

def order_change_status(request, order_id):
    order = get_object_or_404(Order, id=order_id)

    if request.method == "POST":
        if order.status.name == 'IN THE MAKING':
            order.status = Status.objects.get(name='SHIPPED')
            order.shipped_at = timezone.now()
            order.save()
            messages.success(request, "Order #"+ str(order_id) +" status updated to SHIPPED.")
        else:
            messages.warning(request, "Order status cannot be changed.")
        return redirect("manage_orders")
    return redirect("manage_orders")

class ManagerOrderList(ListView):
    model = Order
    template_name = 'manager_order_list.html'
    context_object_name = 'orders'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        orders = Order.objects.all().order_by('-date')

        for order in orders:
            order.update_status()
            order.non_refundable()

        context['orders'] = orders
        return context


def order_return(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user.profile)
    order_products = OrderProduct.objects.filter(order=order)

    if order.status.name == 'RETURNED':
        messages.warning(request, "This order has already been returned.")
        return redirect('order_summary')

    if order.status.name == 'NON REFUNDABLE':
        messages.warning(request, "This order is not refundable.")
        return redirect('order_summary')

    form = ReturnRequestForm(order=order)

    return render(request, 'return_order.html', {
        'form': form,
        'order': order,
        'order_products': order_products
    })

@transaction.atomic
def submit_return_request(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user.profile)

    if request.method == 'POST':
        form = ReturnRequestForm(request.POST, order=order)

        if form.is_valid():
            return_request = form.save(commit=False)
            return_request.user = request.user.profile
            return_request.order = order
            return_request.save()
            form.save_m2m()

            order.status = Status.objects.get(name='RETURNED')
            order.save()

            for order_product in return_request.order_products.all():
                product_stock, created = ProductStock.objects.get_or_create(
                    product=order_product.product,
                    size=order_product.size,
                    defaults={'stock': 0}
                )
                product_stock.stock += order_product.quantity
                product_stock.save()

            messages.success(request, "Return request submitted successfully.")
            return redirect('order_summary')
    else:
        form = ReturnRequestForm(order=order)
    return render(request, 'return_order.html', {'form': form, 'order': order})

def return_requests_for_order(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return_requests = ReturnRequest.objects.filter(order=order)

    context = {
        'order': order,
        'return_requests': return_requests,
    }
    return render(request, 'return_requests_for_order.html', context)



