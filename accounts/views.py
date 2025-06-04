from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login
from .forms import CustomUserCreationForm
from django.contrib.auth.models import Group

def register_view(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            client_group, created = Group.objects.get_or_create(name='client')
            user.groups.add(client_group)
            login(request, user)
            return redirect('frontpage')
    else:
        form = CustomUserCreationForm()
    return render(request, 'register.html', {'form': form})

# Create your views here.

def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('frontpage')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})
