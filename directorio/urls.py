from django.urls import path
from . import views

app_name = 'directorio'
urlpatterns = [
    path('agregar_registro/', views.agregar_registro, name='agregar_registro'),
    path('lista_registros/', views.lista_registros, name='lista_registros')
]