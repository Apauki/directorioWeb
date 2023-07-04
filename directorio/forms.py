from django import forms
from .models import Registro
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

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

    def clean_telefono_institucional(self):
        telefono = self.cleaned_data.get('telefono_institucional')
        if telefono and not telefono.isdigit():
            raise forms.ValidationError('Ingresa solo números en el teléfono institucional.')
        if telefono and len(telefono) > 12:
            raise forms.ValidationError('El teléfono institucional debe tener máximo 12 dígitos.')
        return telefono
    
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
        if extension_telefonica and len(extension_telefonica) > 3:
            raise forms.ValidationError('La extensión telefónica debe tener máximo 3 dígitos.')
        return extension_telefonica
    
class UsuarioForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text='Ingrese su email. Con esto va a iniciar sesión posteriormente')

    class Meta:
        model = User
        fields = ['email', 'password1', 'password2']

class LoginForm(forms.Form):
    email = forms.EmailField(max_length=254, help_text='Ingrese su correo electrónico')
    password = forms.CharField(widget=forms.PasswordInput, help_text='Ingrese su contraseña')