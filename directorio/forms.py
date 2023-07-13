import re
from django import forms
from .models import Registro
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class RegistroForm(forms.ModelForm):
    class Meta:
        model = Registro
        fields = [
            'nombres_apellidos',
            'cedula',
            'puesto_institucional',
            'unidad_pertenece',
            'direccion_institucional',
            'ciudad_labora',
            'telefono_institucional',
            'extension_telefonica',
            'correo_electronico'
        ]
        labels = {
            'nombres_apellidos' : 'Nombres y apellidos',
            'cedula' : 'C.I.',
            'unidad_pertenece' : 'Unidad a la que pertenece',
            'direccion_institucional' : 'Dirección institucional',
            'ciudad_labora' : 'Ciudad en la que labora',
            'telefono_institucional' : 'Teléfono institucional',
            'extension_telefonica' : 'Extensión telefónica',
            'correo_electronico' : 'Correo electrónico',
        }

    def clean_cedula(self):
        cedula = self.cleaned_data.get('cedula')
        if cedula:
            if not re.match(r'^\d+$', cedula):
                raise forms.ValidationError('Ingresa solo números en el campo de cédula.')
            if len(cedula) != 10:
                raise forms.ValidationError('La cédula debe tener exactamente 10 dígitos.')
        return cedula
    
    def clean_correo_electronico(self):
        correo_electronico = self.cleaned_data.get('correo_electronico')
        try:
            validate_email(correo_electronico)
        except ValidationError:
            raise forms.ValidationError('Ingresa una dirección de correo electrónico válida.')
        return correo_electronico
    
    def clean_extension_telefonica(self):
        extension_telefonica = self.cleaned_data.get('extension_telefonica')
        if extension_telefonica and not extension_telefonica.isdigit():
            raise forms.ValidationError('Ingresa solo números en la extensión telefónica.')
        if extension_telefonica and len(extension_telefonica) > 10:
            raise forms.ValidationError('La extensión telefónica debe tener máximo 3 dígitos.')
        return extension_telefonica
    
class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
    