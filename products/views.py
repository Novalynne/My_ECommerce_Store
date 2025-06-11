from django.shortcuts import render, redirect

from .forms import AddToShopForm, SizeStockFormSet
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
        form = AddToShopForm(request.POST, request.FILES)
        formset = SizeStockFormSet(request.POST)
        if form.is_valid() and formset.is_valid():
            name = form.cleaned_data['name']
            description = form.cleaned_data['description']
            price = form.cleaned_data['price']
            category = form.cleaned_data['category']
            is_sale = form.cleaned_data['is_sale']
            sale_price = form.cleaned_data['sale_price']
            image = form.cleaned_data['image']
            product = Product.objects.create(
                name=name,
                description=description,
                price=price,
                image=image,
                is_sale=is_sale,
                sale_price=sale_price
            )
            product.categories.set(category)
            for f in formset:
                f.empty_permitted = False
                size = f.cleaned_data.get('size')
                stock = f.cleaned_data.get('stock')
                if stock is not None:
                    ProductStock.objects.create(
                        product=product,
                        size=size,
                        stock=stock
                    )
            return redirect("homepage")
    else:
        form = AddToShopForm()
        formset = SizeStockFormSet(initial=initial)
    return render(request, 'add_product_to_shop.html', {
        'form': form, 'formset': formset,
        'is_client': user.is_authenticated and user.groups.filter(name='client').exists(),
        'is_manager': user.is_authenticated and user.groups.filter(name='manager').exists(),
        'is_admin': user.is_authenticated and user.is_superuser,
    })

def edit_product(request, pk):
    pass

def delete_product(request, pk):
    pass

