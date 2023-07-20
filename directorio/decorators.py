from functools import wraps
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import redirect
from django.urls import reverse

def custom_login_required(login_url=None):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect(login_url or reverse('login'))
            elif not user_passes_test(lambda u: u.is_superuser)(request.user):
                messages.warning(request, "Inicie sesión como administrador para acceder a esta ventana.")
                return redirect(login_url or reverse('login'))
            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator