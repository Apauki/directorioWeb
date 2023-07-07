from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User
from .forms import UsuarioForm, UserUpdateForm
import logging

logger = logging.getLogger(__name__)

# Register your models here.
class CustomUserAdmin(UserAdmin):
    add_form = UsuarioForm
    form = UsuarioForm
    model = User
    list_display = ['email', 'is_staff']
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )
    ordering = ('email',)
    filter_horizontal = ()

    def save_model(self, request, obj, form, change):
        try:
            super().save_model(request, obj, form, change)
        except Exception as e:
            logger.exception("Error al guardar el modelo:")
            raise e
        
class UserUpdateAdmin(UserAdmin):
    form = UserUpdateForm

admin.site.register(User, CustomUserAdmin)