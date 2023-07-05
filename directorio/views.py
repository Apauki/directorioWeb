from django.shortcuts import render, redirect, get_object_or_404
from .models import Registro, User
from .forms import RegistroForm, UsuarioForm, LoginForm
from django.contrib.auth import login as auth_login
from django.conf import settings
from django.contrib.auth.decorators import login_required

@login_required
def lista_registros(request):
    user = request.user
    registros = Registro.objects.all()
    return render(request, 'directorio/lista_registros.html', {'registros': registros})

def agregar_registro(request):
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('directorio:lista_registros')
    else:
        form = RegistroForm()

    return render(request, 'directorio/agregar_registro.html', {'form': form})

def editar_registro(request, numero_registro):
    registro = get_object_or_404(Registro, numero_registro=numero_registro)

    if request.method == 'POST':
        form = RegistroForm(request.POST, instance=registro)
        if form.is_valid():
            form.save()
            return redirect('directorio:lista_registros')
    else:
        form = RegistroForm(instance=registro)

    return render(request, 'directorio/editar_registro.html', {'form': form})

def eliminar_registro(request, numero_registro):
    registro = get_object_or_404(Registro, numero_registro=numero_registro)
    if request.method == 'POST':
        registro.delete()
        Registro.update_numeros_registro()
        return redirect('directorio:lista_registros')
    return render(request, 'directorio/eliminar_registro.html', {'registro': registro})

def registroUsuario_view(request):
    if request.method == 'POST':
        form = UsuarioForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.email = form.cleaned_data['email']
            user.save()
            auth_login(request, user)
            return redirect('login_view')
    else:
        form = UsuarioForm()
    return render(request, 'registration/registroUsuario.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            user = User.objects.filter(email=email).first()
            if user is not None and user.check_password(password):

                auth_login(request, user)
                return redirect('directorio:lista_registros')
            else:
                error_message = 'Correo electrónico o contraseña incorrectos.'
                return render(request, 'registration/login.html', {'form': form, 'error_message': error_message})
    else:
        form = LoginForm()
    
    context = {
        'form': form
    }
    return render(request, 'registration/login.html', context)
