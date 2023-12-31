from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

from directorio import views as directorio_views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', directorio_views.login_view, name='login'),
    path('directorio/', include('directorio.urls')),
    path('accounts/logout/', directorio_views.logout_view, name='logout'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/register/', directorio_views.registroUsuario_view, name='register'),
]


