from django.shortcuts import render, get_object_or_404, render
from django.contrib import messages
from django.shortcuts import redirect

from accounts.models import Profile
from products.models import Product, ProductStock
from .models import Cart
from django.http import JsonResponse
from django.contrib import messages
from .forms import AddToCartForm
from django.views.generic import ListView
from pages.forms import SearchForm

# Create your views here.
'''

from .cart import Cart
def cart_summary(request):
    # Get the cart
    cart = Cart(request)
    cart_products = cart.get_prods
    quantities = cart.get_quants
    totals = cart.cart_total()
    return render(request, "cart_summary.html",
                  {"cart_products": cart_products, "quantities": quantities, "totals": totals})


def cart_add(request):
    # Get the cart
    cart = Cart(request)
    # test for POST
    if request.POST.get('action') == 'post':
        # Get stuff
        product_id = int(request.POST.get('product_id'))
        product_qty = int(request.POST.get('product_qty'))

        # lookup product in DB
        product = get_object_or_404(Product, id=product_id)

        # Save to session
        cart.add(product=product, quantity=product_qty)

        # Get Cart Quantity
        cart_quantity = cart.__len__()

        # Return resonse
        # response = JsonResponse({'Product Name: ': product.name})
        response = JsonResponse({'qty': cart_quantity})
        messages.success(request, ("Product Added To Cart..."))
        return response


def cart_delete(request):
    cart = Cart(request)
    if request.POST.get('action') == 'post':
        # Get stuff
        product_id = int(request.POST.get('product_id'))
        # Call delete Function in Cart
        cart.delete(product=product_id)

        response = JsonResponse({'product': product_id})
        # return redirect('cart_summary')
        messages.success(request, ("Item Deleted From Shopping Cart..."))
        return response


def cart_update(request):
    cart = Cart(request)
    if request.POST.get('action') == 'post':
        # Get stuff
        product_id = int(request.POST.get('product_id'))
        product_qty = int(request.POST.get('product_qty'))

        cart.update(product=product_id, quantity=product_qty)

        response = JsonResponse({'qty': product_qty})
        # return redirect('cart_summary')
        messages.success(request, ("Your Cart Has Been Updated..."))
        return response


from django.shortcuts import render'''

class cart_summary(ListView):
    model = Cart
    template_name = 'cart_summary.html'
    paginate_by = 10
    context_object_name = 'cart_products'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
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
            # Aggiorna lo stock
            stock.stock -= quantity
            stock.save()
            messages.success(request, "Prodotto aggiunto al carrello!")
            return redirect("product", pk=product_id)
        else:
            messages.error(request, "Dati non validi.")
            return redirect(request.META.get("HTTP_REFERER", "/"))
    return redirect("homepage")
def remove_from_cart(request):
    pass
def update_cart(request):
    pass

