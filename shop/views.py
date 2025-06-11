from django.shortcuts import render, get_object_or_404, render
from django.contrib import messages
from django.shortcuts import redirect

from accounts.models import Profile
from products.models import Product, ProductStock , Size
from .models import Cart
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
        context['cart_products'] = cart_products
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