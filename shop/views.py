from django.shortcuts import render, get_object_or_404, render
from django.shortcuts import redirect
from accounts.models import Profile
from products.models import Product, ProductStock , Size
from .models import Cart, Order
from django.http import JsonResponse
from django.contrib import messages
from .forms import AddToCartForm
from django.views.generic import ListView
from pages.forms import SearchForm

# Create your views here.

class cart_summary(ListView):
    model = Cart
    template_name = 'cart_summary.html'
    paginate_by = 10
    context_object_name = 'cart_products'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        cart_products = Cart.objects.filter(user__user=user)

        total = 0
        for item in cart_products:
            if item.product.is_sale:
                price = item.product.sale_price
            else:
                price = item.product.price
            total += price * item.quantity

        context['cart_products'] = cart_products
        context['total'] = total
        context['is_client'] = user.is_authenticated and user.groups.filter(name='client').exists()
        context['is_manager'] = user.is_authenticated and user.groups.filter(name='manager').exists()
        context['is_admin'] = user.is_authenticated and user.is_superuser
        return context
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
                messages.error(request, "Quantità richiesta non disponibile.")
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
            messages.success(request, "Prodotto aggiunto al carrello!")
            return redirect("product", pk=product_id)
        else:
            messages.error(request, "Dati non validi.")
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
            elif action == "decrease":
                if cart_item.quantity > 1:
                    cart_item.quantity -= 1
                    cart_item.save()
                else:
                    cart_item.delete()
    return redirect("cart_summary")

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
        context['is_client'] = user.is_authenticated and user.groups.filter(name='client').exists()
        context['is_manager'] = user.is_authenticated and user.groups.filter(name='manager').exists()
        context['is_admin'] = user.is_authenticated and user.is_superuser
        return context

def toggle_wishlist(request, product_id):
    user = request.user
    profile = Profile.objects.get(user=user)
    product = get_object_or_404(Product, pk=product_id)
    if product not in profile.favourites.all():
        profile.favourites.add(product)
    else:
        profile.favourites.remove(product)
    return redirect(request.META.get('HTTP_REFERER', 'homepage'))

from decimal import Decimal
from django.shortcuts import redirect, render
from django.contrib import messages
from .models import Cart, Order, OrderProduct, Profile

def place_order(request):
    user = request.user
    profile = Profile.objects.get(user=user)
    cart_items = Cart.objects.filter(user=profile)

    if request.method == "POST":
        if not cart_items.exists():
            return redirect("cart_summary")

        order = Order.objects.create(
            user=profile,
            address=profile.address,
            total=Decimal('0.00'),
            status_id= 1
        )

        order_products = []
        for item in cart_items:
            order_product = OrderProduct(
                order=order,
                product=item.product,
                quantity=item.quantity,
                size=item.size,
                unit_price=item.product.price if not item.product.is_sale else item.product.sale_price
            )
            order_products.append(order_product)
            product_stock = ProductStock.objects.get(product=item.product, size=item.size)
            if product_stock.stock >= item.quantity:
                product_stock.stock -= item.quantity
                product_stock.save()
                if product_stock.stock <= 0:
                    product_stock.delete()
                    return redirect("cart_summary")
            else:
                return redirect("cart_summary")

        OrderProduct.objects.bulk_create(order_products)

        total = sum(op.unit_price * op.quantity for op in order.products.all())
        order.total = total
        order.save()


        cart_items.delete()

        return redirect("order_summary")
    return redirect("cart_summary")

class order_summery(ListView):
    model = Order
    template_name = 'order_summary.html'
    context_object_name = 'orders'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        orders = Order.objects.filter(user__user=user).order_by('-date')

        context['orders'] = orders
        context['is_client'] = user.is_authenticated and user.groups.filter(name='client').exists()
        context['is_manager'] = user.is_authenticated and user.groups.filter(name='manager').exists()
        context['is_admin'] = user.is_authenticated and user.is_superuser
        return context