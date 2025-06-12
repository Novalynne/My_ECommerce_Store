from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib.auth import login, logout, update_session_auth_hash
from .forms import CustomUserCreationForm, EditProfileForm
from django.contrib.auth.models import Group
from django.views.generic import ListView, DetailView
from .models import Profile

def register_view(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            client_group, created = Group.objects.get_or_create(name='client')
            user.groups.add(client_group)
            return redirect('login')
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
            return redirect('homepage')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('frontpage')

class profile(DetailView):
    model = Profile
    template_name = 'account_details.html'
    context_object_name = 'profile'

    def get_object(self, queryset=None):
        return Profile.objects.get(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        profile = Profile.objects.get(user=user)
        context['profile'] = profile
        context['is_client'] = user.is_authenticated and user.groups.filter(name='client').exists()
        context['is_manager'] = user.is_authenticated and user.groups.filter(name='manager').exists()
        context['is_admin'] = user.is_authenticated and user.is_superuser
        return context

def edit_profile_view(request):
    user = request.user
    if request.method == "POST":
        if 'save_profile' in request.POST:
            profile_form = EditProfileForm(request.POST, instance=user, user=user)
            password_form = PasswordChangeForm(user)
            if profile_form.is_valid():
                profile_form.save(user)
                return redirect('profile')
        elif 'change_password' in request.POST:
            password_form = PasswordChangeForm(user, request.POST)
            profile_form = EditProfileForm(instance=user, user=user)
            if password_form.is_valid():
                user = password_form.save()
                update_session_auth_hash(request, user)
                return redirect('profile')
    else:
        profile_form = EditProfileForm(instance=request.user, user=request.user)
        password_form = PasswordChangeForm(request.user)
    return render(request, 'edit_profile.html', {
        'profile_form': profile_form,
        'password_form': password_form,
        'is_client': user.is_authenticated and user.groups.filter(name='client').exists(),
        'is_manager': user.is_authenticated and user.groups.filter(name='manager').exists(),
        'is_admin': user.is_authenticated and user.is_superuser,
    })

def delete_profile_view(request):
    if request.method == "POST":
        if 'confirm_delete' in request.POST:
            user = request.user
            user.delete()
            logout(request)
            return redirect('frontpage')
    return redirect('edit_profile')

