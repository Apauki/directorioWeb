from django.urls import path
from directorio import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'directorio'
urlpatterns = [
    path('agregar_registro/', views.agregar_registro, name='agregar_registro'),
    path('lista_registros/', views.lista_registros, name='lista_registros'),
    path('editar_registro/<int:numero_registro>/', views.editar_registro, name='editar_registro'),
    path('eliminar_registro/<int:numero_registro>/', views.eliminar_registro, name='eliminar_registro'),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
