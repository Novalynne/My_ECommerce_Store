from django import forms
from django.core.validators import MinValueValidator
from decimal import Decimal
from django.forms import formset_factory
from .models import Category, Size, Product

class SizeStockForm(forms.Form):
    size = forms.ModelChoiceField(queryset=Size.objects.all(), widget=forms.HiddenInput())
    stock = forms.IntegerField(min_value=0, required=False, label="Stock for Size", widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter stock quantity for this size'}))


SizeStockFormSet = formset_factory(SizeStockForm, extra=0, can_delete=False)

class ProductForm(forms.ModelForm):
    categories = forms.ModelMultipleChoiceField(
        queryset=Category.objects.all(),
        required=True,
        widget=forms.CheckboxSelectMultiple,
    )

    def clean(self):
        cleaned_data = super().clean()
        is_sale = cleaned_data.get('is_sale')
        sale_price = cleaned_data.get('sale_price')
        price = cleaned_data.get('price')
        if is_sale:
            if sale_price is None:
                self.add_error('sale_price', "Sale price is required when the product is on sale.")
            elif price is not None and sale_price >= price:
                self.add_error('sale_price', "Sale price must be less than the regular price.")
        elif sale_price is not None:
            self.add_error('sale_price', "Sale price should not be set if the product is not on sale.")
        return cleaned_data

    def clean_name(self):
        name = self.cleaned_data.get('name')
        qs = Product.objects.filter(name=name)
        if self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise forms.ValidationError("A product with this name already exists.")
        return name

    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'categories', 'is_sale', 'sale_price', 'image']