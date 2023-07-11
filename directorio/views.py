from django.shortcuts import render, redirect, get_object_or_404
from .models import Registro
from .forms import RegistroForm
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.decorators import login_required, user_passes_test

def es_superusuario(user):
    return user.is_superuser

@login_required
def lista_registros(request):
    user = request.user
    registros = Registro.objects.all()
    return render(request, 'directorio/lista_registros.html', {'registros': registros, 'user': request.user})

@user_passes_test(es_superusuario)
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
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            return redirect('login')  # Redirigir a la página de login después del registro
    else:
        form = UserCreationForm()
    
    return render(request, 'registration/registroUsuario.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('directorio/lista_registros')  # Redirigir a la página de lista_registros después del inicio de sesión
    else:
        form = AuthenticationForm()
    return render(request, 'registration/login.html', {'form':form})

def logout_view(request):
    logout(request)
    return redirect('login')
