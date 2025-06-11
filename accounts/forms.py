from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile

class CustomUserCreationForm(UserCreationForm):

    email = forms.EmailField(required=True)
    address = forms.CharField(required=True)
    phone_number = forms.CharField(required=False)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'address', 'phone_number']


    def clean_phone_number(self):
        phone = self.cleaned_data.get("phone_number")
        if not phone:
            return phone
        if not phone.isdigit():
            raise forms.ValidationError("The phone number must not contain letters.")
        if len(phone) != 10:
            raise forms.ValidationError("The phone number must be 10 cifre long.")
        if Profile.objects.filter(phone_number=phone).exists():
            raise forms.ValidationError("This phone number is already in use.")
        return phone

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("This email is already in use.")
        return email

    def clean_username(self):
        username = self.cleaned_data.get("username")
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("This username is already taken.")
        return username

    def save(self, commit=True):
        user = super().save(commit=commit)
        profile = user.profile
        profile.address = self.cleaned_data['address']
        phone_number = self.cleaned_data['phone_number']
        profile.phone_number = phone_number if phone_number else None
        if commit:
            profile.save()
        return user


class EditProfileForm(forms.ModelForm):
    username = forms.CharField(required=True, label="Username")
    first_name = forms.CharField(required=False, label="Name")
    last_name = forms.CharField(required=False, label="Surname")
    email = forms.EmailField(required=True, label="Email")
    address = forms.CharField(required=True, label="Address")
    phone_number = forms.CharField(required=False, label="Phone Number")
    class Meta:
        model = Profile
        fields = ['username', 'first_name', 'last_name', 'email', 'address', 'phone_number']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            self.fields['username'].initial = self.instance.username
            self.fields['first_name'].initial = self.instance.first_name
            self.fields['last_name'].initial = self.instance.last_name
            self.fields['email'].initial = self.instance.email
            self.fields['address'].initial = self.instance.profile.address
            self.fields['phone_number'].initial = self.instance.profile.phone_number

    def clean_phone_number(self):
        phone = self.cleaned_data.get("phone_number")
        if not phone:
            return phone
        if not phone.isdigit():
            raise forms.ValidationError("The phone number must not contain letters.")
        if len(phone) != 10:
            raise forms.ValidationError("The phone number must be 10 cifre long.")
        if Profile.objects.filter(phone_number=phone).exclude(user=self.instance).exists():
            raise forms.ValidationError("This phone number is already in use.")
        return phone

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if User.objects.filter(email=email).exclude(id=self.instance.id).exists():
            raise forms.ValidationError("This email is already in use.")
        return email

    def clean_username(self):
        username = self.cleaned_data.get("username")
        if User.objects.filter(username=username).exclude(id=self.instance.id).exists():
            raise forms.ValidationError("This username is already taken.")
        return username

    def save(self, commit=True):
        user = super().save(commit=commit)
        profile = user.profile
        user.username = self.cleaned_data['username']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']
        profile.address = self.cleaned_data['address']
        phone_number = self.cleaned_data['phone_number']
        profile.phone_number = phone_number if phone_number else None
        if commit:
            user.save()
            profile.user = user
            profile.save()
        return profile
