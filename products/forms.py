from django import forms
from django.core.validators import MinValueValidator
from decimal import Decimal
from django.forms import formset_factory
from .models import Category, Size, Product

class SizeStockForm(forms.Form):
    size = forms.ModelChoiceField(queryset=Size.objects.all(), widget=forms.HiddenInput())
    stock = forms.IntegerField(min_value=0, required=False, label="Stock for Size", widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter stock quantity for this size'}))


SizeStockFormSet = formset_factory(SizeStockForm, extra=0, can_delete=False)

class AddToShopForm(forms.Form): #Old version of ProductForm

    name = forms.CharField(max_length=100, required=True, label="Product Name", widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter product name'}))
    description = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Enter product description'}), required=True, label="Description")
    price = forms.DecimalField(max_digits=10, min_value=0.00, decimal_places=2, required=True, label="Price", widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter product price'}))
    category = forms.ModelMultipleChoiceField(
        queryset=Category.objects.all(),
        required=True,
        widget=forms.CheckboxSelectMultiple,
    )
    is_sale = forms.BooleanField(required=False, label="Is on Sale", widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}))
    sale_price = forms.DecimalField(max_digits=10, min_value=0.00, decimal_places=2, required=False, label="Sale Price", widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter sale price'}))
    image = forms.ImageField(required=True, label="Product Image", widget=forms.ClearableFileInput(attrs={'class': 'form-control-file'}))

    def clean_sale_price(self):
        is_sale = self.cleaned_data.get('is_sale')
        sale_price = self.cleaned_data.get('sale_price')
        price = self.cleaned_data.get('price')
        if is_sale and sale_price is None:
            raise forms.ValidationError("Sale price is required when the product is on sale.")
        if is_sale and sale_price >= price:
            raise forms.ValidationError("Sale price must be less than the regular price.")
        if not is_sale and sale_price is not None:
            raise forms.ValidationError("Sale price should not be set if the product is not on sale.")
        return sale_price

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if Product.objects.filter(name=name).exists():
            raise forms.ValidationError("A product with this name already exists.")
        return name



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