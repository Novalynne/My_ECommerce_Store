from django import forms
from products.models import Size

class AddToCartForm(forms.Form):
    size = forms.ModelChoiceField(queryset=Size.objects.all(), required=True, label="Size")
    quantity = forms.IntegerField(min_value=1, initial=1, label="Quantity", widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter quantity'}))