from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

from directorio import views as directorio_views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('directorio/', include('directorio.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/register/', directorio_views.registroUsuario_view, name='register'),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
