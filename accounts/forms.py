from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile

class CustomUserCreationForm(UserCreationForm):

    address = forms.CharField(required=True)
    phone_number = forms.CharField(required=False)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=commit)
        # Assumiamo che il segnale `post_save` abbia già creato il Profile
        profile = user.profile
        profile.address = self.cleaned_data['address']
        profile.phone_number = self.cleaned_data['phone_number']
        if commit:
            profile.save()
        return user

