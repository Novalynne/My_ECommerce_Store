from django.shortcuts import render
from .models import Product, ProductStock, Size
from shop.forms import AddToCartForm

# Create your views here.

def product(request,pk):
    product = Product.objects.get(id=pk)
    size = ProductStock.objects.filter(product=product)
    form = AddToCartForm()
    available_sizes = [ps.size for ps in size]
    form.fields['size'].queryset = Size.objects.filter(pk__in=[size.pk for size in available_sizes])
    user = request.user
    context = {
        'product': product,
        'sizes': size,
        'form': form,
        'is_client': user.is_authenticated and user.groups.filter(name='client').exists(),
        'is_manager': user.is_authenticated and user.groups.filter(name='manager').exists(),
        'is_admin': user.is_authenticated and user.is_superuser,
    }
    return render(request, 'product.html', context)