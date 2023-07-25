import re
from django.shortcuts import render, redirect, get_object_or_404
from .models import Registro
from .forms import RegistroForm, CustomUserCreationForm
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.db.models import Q
from django.contrib.auth.decorators import login_required, user_passes_test


# Constantes para identificar los campos de ordenamiento
ORDEN_ALFABETICO = 'nombres_apellidos'
ORDEN_NUMERO_REGISTRO = 'numero_registro'
ORDEN_UNIDAD_PERTENECE = 'unidad_pertenece'


'''
def es_superusuario(user):
    return user.is_superuser
'''

def remover_caracteres_especiales(cadena):
    # Utilizar una expresión regular para eliminar los caracteres especiales
    return re.sub(r'[^a-zA-Z0-9]', '', cadena)


@login_required
def lista_registros(request):

    user = request.user
    registros = Registro.objects.all()

    #Búsqueda de registro (query)
    search_query = request.GET.get('search_query', '')
    if search_query:
        filtro_busqueda =   Q(nombres_apellidos__icontains=search_query) | \
                            Q(cedula__icontains=search_query) | \
                            Q(correo_electronico__icontains=search_query) | \
                            Q(unidad_pertenece__icontains=search_query)
        registros = Registro.objects.filter(filtro_busqueda)

    # Filtro de ordenamiento
    ordenar_por = request.GET.get('ordenar_por', 'numero_registro')
    registros = registros.order_by(ordenar_por)
        
    context = {
        'registros': registros,
        'user': request.user,
        'search_query': search_query,
        'ordenar_por': ordenar_por,
    }

    return render(request, 'directorio/lista_registros.html', context)


def agregar_registro(request):

    if not request.user.is_superuser:
        messages.add_message(request, messages.WARNING, "Inicie sesión como administrador para acceder a esta ventana.")
        return redirect('login')

    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('directorio:lista_registros')
    else:
        form = RegistroForm()

    return render(request, 'directorio/agregar_registro.html', {'form': form})


def editar_registro(request, numero_registro):

    if not request.user.is_superuser:
        messages.add_message(request, messages.WARNING, "Inicie sesión como administrador para acceder a esta ventana.")
        return redirect('login')

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

    if not request.user.is_superuser:
        messages.add_message(request, messages.WARNING, "Inicie sesión como administrador para acceder a esta ventana.")
        return redirect('login')

    registro = get_object_or_404(Registro, numero_registro=numero_registro)
    if request.method == 'POST':
        registro.delete()
        Registro.update_numeros_registro()
        return redirect('directorio:lista_registros')
    return render(request, 'directorio/eliminar_registro.html', {'registro': registro})

def registroUsuario_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            return redirect('login')  # Redirigir a la página de login después del registro
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'registration/registroUsuario.html', {'form': form})

#Iniciar sesión
@login_required
def login_view(request):

    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)           
            return redirect('directorio:lista_registros') # Redirigir a la página de lista_registros después del inicio de sesión
    else:
        form = AuthenticationForm()
    return render(request, 'registration/login.html', {'form':form})

# Cerrar sesión
def logout_view(request):
    logout(request)
    return redirect('login')
