from django.shortcuts import render,  redirect, get_object_or_404
from django.views.generic.list import ListView

from accounts.models import Profile
from products.models import Product, Category, Size, ProductStock
from pages.forms import SearchForm

# Create your views here.

def frontpage(request):
    return render(request, 'front_page.html')

class homepage(ListView): #TODO: FIX SEARCH FUNCTIONALITY
    model = Product
    template_name = 'home_page.html'
    paginate_by = 10
    context_object_name = 'products'

    def get_queryset(self):
        queryset = super().get_queryset()
        search_form = SearchForm(self.request.GET or None)
        print("GET params:", self.request.GET)
        if search_form.is_valid():
            search = search_form.cleaned_data.get("search")
            print("Search term:", search)
            categories = search_form.cleaned_data.get('category')
            print("Selected categories:", categories)
            sizes = search_form.cleaned_data.get('size')
            print("Selected sizes:", sizes)
            min_price = search_form.cleaned_data.get('min_price')
            print("Minimum price:", min_price)
            max_price = search_form.cleaned_data.get('max_price')
            print("Maximum price:", max_price)
            if search:
                queryset = queryset.filter(name__icontains=search)

            if categories:
                queryset = queryset.filter(categories__in=categories)

            if sizes:
                queryset = queryset.filter(stock__size__in=sizes)

            if min_price is not None:
                queryset = queryset.filter(price__gte=min_price)

            if max_price is not None:
                queryset = queryset.filter(price__lte=max_price)

            queryset = queryset.distinct()

        return queryset
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        profile = Profile.objects.get(user=user)
        favourite = profile.favourites.all()
        context['favourites'] = favourite
        context['search_form'] = SearchForm(self.request.GET)
        context['is_client'] = user.is_authenticated and user.groups.filter(name='client').exists()
        context['is_manager'] = user.is_authenticated and user.groups.filter(name='manager').exists()
        context['is_admin'] = user.is_authenticated and user.is_superuser
        return context

'''
def search_page_view(request):
    if request.method == "POST":
        search_form = SearchForm(request.POST)
        products = Product.objects.all()
        if search_form.is_valid():
            search = search_form.cleaned_data["search"]
            category = search_form.cleaned_data['category']
            size = search_form.cleaned_data['size']
            min_price = search_form.cleaned_data['min_price']
            max_price = search_form.cleaned_data['max_price']

            if search is not None:
                products = products.filter(name__icontains=search)

            if category is not None:
                products = products.filter(category=category)

            if size is not None:
                products = products.filter(size=size)

            if min_price is not None:
                products = products.filter(price__gte=min_price)

            if max_price is not None:
                products = products.filter(price__lte=max_price)

            return render(request, 'home_page.html', {
                'search_form': search_form,
                'products': products})

    else:
        search_form = SearchForm()
        return redirect(request, "homepage", {"form": search_form})
'''
