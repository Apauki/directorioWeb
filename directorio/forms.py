from django import forms
from .models import Registro

class RegistroForm(forms.ModelForm):
    class Meta:
        model = Registro
        fields = [
            'nombres_apellidos',
            'puesto_institucional',
            'unidad_pertenece',
            'direccion_institucional',
            'ciudad_labora',
            'telefono_institucional',
            'extension_telefonica',
            'correo_electronico'
        ]