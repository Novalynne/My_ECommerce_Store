from django.shortcuts import render,  redirect, get_object_or_404
from django.views.generic.list import ListView
from products.models import Product, Category, Size, ProductStock


# Create your views here.

def frontpage(request):
    return render(request, 'front_page.html')

class homepage(ListView):
    model = Product
    template_name = 'home_page.html'
    paginate_by = 10
    context_object_name = 'products'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context['is_client'] = user.is_authenticated and user.groups.filter(name='client').exists()
        context['is_manager'] = user.is_authenticated and user.groups.filter(name='manager').exists()
        context['is_admin'] = user.is_authenticated and user.is_superuser
        return context

