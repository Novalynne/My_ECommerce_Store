from django.shortcuts import render, redirect, get_object_or_404

from .forms import AddToShopForm, SizeStockFormSet, ProductForm
from .models import Product, ProductStock, Size
from shop.forms import AddToCartForm
from accounts.models import Profile

# Create your views here.

def product(request,pk):
    product = Product.objects.get(id=pk)
    size = ProductStock.objects.filter(product=product)
    form = AddToCartForm()
    available_sizes = [ps.size for ps in size]
    form.fields['size'].queryset = Size.objects.filter(pk__in=[size.pk for size in available_sizes])
    user = request.user
    profile = Profile.objects.get(user=user)
    favorites = profile.favourites.all()
    context = {
        'favorites': favorites,
        'product': product,
        'sizes': size,
        'form': form,
        'is_client': user.is_authenticated and user.groups.filter(name='client').exists(),
        'is_manager': user.is_authenticated and user.groups.filter(name='manager').exists(),
        'is_admin': user.is_authenticated and user.is_superuser,
    }
    return render(request, 'product.html', context)

def category(request, foo):
    pass

def category_summary(request):
    pass

def add_to_shop(request):
    user = request.user
    sizes = Size.objects.all()
    initial = [{'size': s} for s in sizes]
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES)
        formset = SizeStockFormSet(request.POST)
        if form.is_valid() and formset.is_valid():
            product = form.save()
            product.categories.set(form.cleaned_data['categories'])
            for f in formset:
                f.empty_permitted = False
                size = f.cleaned_data.get('size')
                stock = f.cleaned_data.get('stock')
                if stock is not None and stock > 0:  # Check if stock is provided and greater than 0
                    ProductStock.objects.create(
                        product=product,
                        size=size,
                        stock=stock
                    )
            return redirect("homepage")
    else:
        form = ProductForm()
        formset = SizeStockFormSet(initial=initial)
    return render(request, 'add_product_to_shop.html', {
        'form': form, 'formset': formset,
        'is_client': user.is_authenticated and user.groups.filter(name='client').exists(),
        'is_manager': user.is_authenticated and user.groups.filter(name='manager').exists(),
        'is_admin': user.is_authenticated and user.is_superuser,
    })

def edit_product(request, pk):
    user = request.user
    product = get_object_or_404(Product, pk=pk)
    sizes = Size.objects.all()
    initial = []
    for size in sizes:
        stock_obj = ProductStock.objects.filter(product=product, size=size).first() # preparo i miei formset iniziali
        initial.append({
            'size': size,
            'stock': stock_obj.stock if stock_obj else None
        })
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES, instance=product)
        formset = SizeStockFormSet(request.POST)
        if form.is_valid() and formset.is_valid():
            product = form.save()
            product.categories.set(form.cleaned_data['categories'])
            for f in formset:
                size = f.cleaned_data.get('size')
                stock = f.cleaned_data.get('stock')
                # Salva solo se stock è valorizzato e > 0
                if size is not None and stock is not None and stock > 0:
                    stock_obj, _ = ProductStock.objects.get_or_create(product=product, size=size)
                    stock_obj.stock = stock if stock is not None else 0
                    stock_obj.save()
                # Se esisteva uno stock ma ora è vuoto o 0, lo elimina
                elif size is not None and (stock is None or stock == 0):
                    ProductStock.objects.filter(product=product, size=size).delete()
            return redirect("homepage")
    else:
        form = ProductForm(instance=product)
        formset = SizeStockFormSet(initial=initial)
    return render(request, 'edit_product.html', {
        'form': form,
        'formset': formset,
        'product': product,
        'is_client': user.is_authenticated and user.groups.filter(name='client').exists(),
        'is_manager': user.is_authenticated and user.groups.filter(name='manager').exists(),
        'is_admin': user.is_authenticated and user.is_superuser,
    })


def delete_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == "POST" and 'confirm_delete' in request.POST:
        product.delete()
        return redirect("homepage")
    return redirect("edit_product", pk=pk)


