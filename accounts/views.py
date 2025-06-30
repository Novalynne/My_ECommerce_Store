from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib.auth import login, logout, update_session_auth_hash
from .forms import CustomUserCreationForm, EditProfileForm
from django.contrib.auth.models import Group, User
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
    })

def delete_profile_view(request):
    if request.method == "POST":
        if 'confirm_delete' in request.POST:
            user = request.user
            user.delete()
            logout(request)
            return redirect('frontpage')
    return redirect('edit_profile')

class ManageProfilesView(ListView):
    model = Profile
    template_name = 'managers.html'
    context_object_name = 'profiles'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        query = self.request.GET.get('q')
        base_clients = Profile.objects.filter(user__groups__name='client')
        base_managers = Profile.objects.filter(user__groups__name='manager')
        if query:
            base_clients = base_clients.filter(user__username__icontains=query)
            base_managers = base_managers.filter(user__username__icontains=query)

        context['clients'] = base_clients
        context['managers'] = base_managers
        context['query'] = query
        return context

def promote_to_manager(request, user_id):
    user = get_object_or_404(User, id=user_id)
    client_group = Group.objects.get(name="client")
    manager_group = Group.objects.get(name="manager")
    if request.method == "POST":
        user.groups.remove(client_group)
        user.groups.add(manager_group)
        return redirect("manage_profiles")
    return render(request, 'managers.html', {'user': user})

def demote_to_client(request, user_id):
    user = get_object_or_404(User, id=user_id)
    client_group = Group.objects.get(name="client")
    manager_group = Group.objects.get(name="manager")

    if request.method == "POST":
        user.groups.remove(manager_group)
        user.groups.add(client_group)
        return redirect("manage_profiles")
    return render(request, 'managers.html', {'user': user})