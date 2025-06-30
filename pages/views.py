from django.shortcuts import render
from django.views.generic.list import ListView
from django.db.models import Q
from accounts.models import Profile
from products.models import Product
from pages.forms import SearchForm

# Create your views here.

def frontpage(request):
    return render(request, 'front_page.html')

class homepage(ListView):
    model = Product
    template_name = 'home_page.html'
    paginate_by = 10
    context_object_name = 'products'

    def get_queryset(self):
        queryset = super().get_queryset()
        search_form = SearchForm(self.request.GET or None)
        if search_form.is_valid():
            search = search_form.cleaned_data.get("search")
            categories = search_form.cleaned_data.get('category')
            sizes = search_form.cleaned_data.get('size')
            min_price = search_form.cleaned_data.get('min_price')
            max_price = search_form.cleaned_data.get('max_price')
            if search:
                queryset = queryset.filter(name__icontains=search)

            if categories:
                queryset = queryset.filter(categories__in=categories)

            if sizes:
                queryset = queryset.filter(product__size__in=sizes)

            if min_price is not None:
                queryset = queryset.filter(
                    Q(sale_price__gte=min_price) |
                    Q(sale_price__isnull=True, price__gte=min_price)
                )

            if max_price is not None:
                queryset = queryset.filter(
                    Q(sale_price__lte=max_price) |
                    Q(sale_price__isnull=True, price__lte=max_price)
                )

            queryset = queryset.distinct()

        return queryset
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        profile = Profile.objects.get(user=user)
        favourite = profile.favourites.all()
        context['favourites'] = favourite
        context['search_form'] = SearchForm(self.request.GET)
        return context