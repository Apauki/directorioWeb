from django.urls import path
from . import views

urlpatterns = [
    path('nuevo/', views.agregar_registro, name='agregar_registro'),
]