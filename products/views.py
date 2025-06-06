from django.shortcuts import render
from .models import Product
# Create your views here.

def product(request,pk):
    product = Product.objects.get(id=pk)
    user = request.user
    context = {
        'product': product,
        'is_client': user.is_authenticated and user.groups.filter(name='client').exists(),
        'is_manager': user.is_authenticated and user.groups.filter(name='manager').exists(),
        'is_admin': user.is_authenticated and user.is_superuser,
    }
    return render(request, 'product.html', context)