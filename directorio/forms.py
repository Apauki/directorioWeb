import re
from django import forms
from .models import Registro, User
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserChangeForm

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
        if telefono:
            if not re.match(r'^[0-9()\-\s]+$', telefono):
                raise forms.ValidationError('Ingresa solo números y caracteres especiales en el teléfono institucional.')
            if len(telefono) > 14:
                raise forms.ValidationError('El teléfono institucional debe tener máximo 14 caracteres. (incluyendo espacios y caracteres especiales)')
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
        if extension_telefonica and len(extension_telefonica) > 10:
            raise forms.ValidationError('La extensión telefónica debe tener máximo 3 dígitos.')
        return extension_telefonica
    
class UsuarioForm(forms.ModelForm):
    email = forms.EmailField(max_length=254, help_text='Ingrese su email. Con esto va a iniciar sesión posteriormente')
    password1 = forms.CharField(label='Contraseña', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirmar contraseña', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['email', 'password1', 'password2']

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Las contraseñas no coinciden.")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user

class LoginForm(forms.Form):
    email = forms.EmailField(max_length=254, help_text='Ingrese su correo electrónico')
    password = forms.CharField(widget=forms.PasswordInput, help_text='Ingrese su contraseña')

class UserUpdateForm(UserChangeForm):
    is_staff = forms.BooleanField(label=_('Staff status'), required=False)
    is_superuser = forms.BooleanField(label=_('Superuser status'), required=False)

    class Meta:
        model = User
        fields = ['email', 'password']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['is_staff'].initial = self.instance.is_staff
        self.fields['is_superuser'].initial = self.instance.is_superuser

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_staff = self.cleaned_data['is_staff']
        user.is_superuser = self.cleaned_data['is_superuser']
        if commit:
            user.save()
            self.save_m2m()
        return user