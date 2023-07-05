from django.contrib import admin
from django.urls import path, include
from directorio import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('directorio/', include('directorio.urls')),
    path('accounts/register/', views.registroUsuario_view, name='registro_usuario'),
    path('accounts/login/', views.login_view, name='login_view'),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
