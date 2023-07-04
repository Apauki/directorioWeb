from django.contrib import admin
from django.urls import path, include
from directorio import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('directorio/', include('directorio.urls')),
    path('accounts/login/', views.custom_login, name='login'),
    path('accounts/register/', views.registroUsuario_view, name='register'),
]
