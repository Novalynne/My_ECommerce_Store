from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile

class CustomUserCreationForm(UserCreationForm):

    address = forms.CharField(required=True)
    phone_number = forms.CharField(required=False)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'address', 'phone_number']


    def clean_phone_number(self):
        phone = self.cleaned_data.get("phone_number")
        if not phone.isdigit():
            raise forms.ValidationError("The phone number must not contain letters.")
        if len(phone) != 10:
            raise forms.ValidationError("The phone number must be 10 cifre long.")
        return phone

    def save(self, commit=True):
        user = super().save(commit=commit)
        profile = user.profile
        profile.address = self.cleaned_data['address']
        profile.phone_number = self.cleaned_data['phone_number']
        if commit:
            profile.save()
        return user

