def user_roles(request):
    user = request.user
    return {
        'is_client': user.is_authenticated and user.groups.filter(name='client').exists(),
        'is_manager': user.is_authenticated and user.groups.filter(name='manager').exists(),
        'is_admin': user.is_authenticated and user.is_superuser,
    }
