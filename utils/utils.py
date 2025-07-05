
def is_client(user):
    return user.is_authenticated and user.groups.filter(name='client').exists()

def is_manager(user):
    return user.is_authenticated and user.groups.filter(name='manager').exists()

def is_admin(user):
    return user.is_authenticated and user.is_superuser

def is_manager_or_admin(user):
    return user.is_authenticated and (
        user.groups.filter(name='manager').exists() or user.is_superuser
    )

