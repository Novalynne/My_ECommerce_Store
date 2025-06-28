from django import forms
from products.models import Size
from shop.models import ReturnRequest, OrderProduct


class AddToCartForm(forms.Form):
    size = forms.ModelChoiceField(queryset=Size.objects.all(), required=True, label="Size")
    quantity = forms.IntegerField(min_value=1, initial=1, label="Quantity", widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter quantity'}))

class ReturnRequestForm(forms.ModelForm):
    order_products = forms.ModelMultipleChoiceField(
        queryset=OrderProduct.objects.none(),
        label='Products and Sizes',
        widget=forms.CheckboxSelectMultiple
    )

    class Meta:
        model = ReturnRequest
        fields = ['order_products', 'reason', 'notes']
        widgets = {
            'reason': forms.Select(attrs={'class': 'form-select'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        order = kwargs.pop('order', None)
        super().__init__(*args, **kwargs)
        if order:
            self.fields['order_products'].queryset = OrderProduct.objects.filter(order=order)
        # Label personalizzata per mostrare "Product - Size"
        self.fields['order_products'].label_from_instance = lambda obj: f"{obj.product.name} - {obj.size}"
