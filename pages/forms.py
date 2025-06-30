from django import forms
from django.forms import ChoiceField
from products.models import Category, Size


class SearchForm(forms.Form):

    search = forms.CharField(label="Search", max_length=110, required=False, widget=forms.TextInput(attrs={'placeholder': 'Type your search'}))
    category = forms.ModelMultipleChoiceField(
        queryset=Category.objects.all(),
        required=False,
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'category-checkboxes'})
    )
    size = forms.ModelMultipleChoiceField(
        queryset=Size.objects.all(),
        required=False,
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'size-checkboxes'})
    )
    min_price = forms.DecimalField(label='Minimum Price', required=False, min_value=0,  widget=forms.NumberInput(attrs={'placeholder': 'Min €'}))
    max_price = forms.DecimalField(label='Maximum Price', required=False, min_value=0,  widget=forms.NumberInput(attrs={'placeholder': 'Max €'}))