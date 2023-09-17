import re
import openpyxl
import csv
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.db.models import Q
from django.db.models.functions import Lower
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

from unidecode import unidecode

from .models import Registro
from .forms import RegistroForm, CustomUserCreationForm


'''
def es_superusuario(user):
    return user.is_superuser
'''

# Función para ordenamiento insensible a caracteres especiales
def remover_caracteres_especiales(cadena):
    # Utilizar una expresión regular para eliminar los caracteres especiales
    return re.sub(r'[^a-zA-Z0-9]', '', cadena)

def normalize_string(string):
    return unidecode(string).lower()


@login_required
def lista_registros(request):

    user = request.user
    registros = Registro.objects.all()

    #Búsqueda de registro (query)
    search_query = request.GET.get('search_query', '')
    if search_query:
        filtro_busqueda =   Q(nombres_apellidos__icontains=search_query) | \
                            Q(cedula__icontains=search_query) | \
                            Q(puesto_institucional__icontains=search_query) | \
                            Q(unidad_pertenece__icontains=search_query) | \
                            Q(direccion_institucional__icontains=search_query) | \
                            Q(ciudad_labora__icontains=search_query) | \
                            Q(telefono_institucional__icontains=search_query) | \
                            Q(extension_telefonica__icontains=search_query) | \
                            Q(correo_electronico__icontains=search_query)

        registros = Registro.objects.filter(filtro_busqueda)

    # Filtro de ordenamiento
    ordenar_por = request.GET.get('ordenar_por', 'numero_registro')

    if ordenar_por == 'nombres_apellidos':
        registros = registros.annotate(nombres_apellidos_lower=Lower('nombres_apellidos'))
        registros = sorted(registros, key=lambda registro: remover_caracteres_especiales(registro.nombres_apellidos_lower))
    else:
        # Ordenar por el campo especificado sin aplicar ordenamiento sensible al idioma
        registros = registros.order_by(ordenar_por)

    # Funciones para generar reporte
    if 'excel' in request.GET:
        return generar_reporte_excel(registros)
    elif 'csv' in request.GET:
        return generar_reporte_csv(registros)

        
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

# Creación de reporte Excel y CSV
def generar_reporte_excel(registros):
    libro = openpyxl.Workbook()
    hoja = libro.active
    hoja.append(['N°', 'Apellidos y Nombres', 'Cédula', 'Puesto Institucional', 'Unidad a la que Pertenece',
                 'Dirección Institucional', 'Ciudad en la que Labora', 'Teléfono Institucional', 'Extensión Telefónica',
                 'Correo Electrónico'])

    for registro in registros:
        hoja.append([registro.numero_registro, registro.nombres_apellidos, registro.cedula,
                     registro.puesto_institucional, registro.unidad_pertenece, registro.direccion_institucional,
                     registro.ciudad_labora, registro.telefono_institucional, registro.extension_telefonica,
                     registro.correo_electronico])

    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=directorio_inamhi.xlsx'
    libro.save(response)
    return response

def generar_reporte_csv(registros):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=directorio_inamhi.csv'

    writer = csv.writer(response)
    writer.writerow(['N°', 'Apellidos y Nombres', 'Cédula', 'Puesto Institucional', 'Unidad a la que Pertenece',
                     'Dirección Institucional', 'Ciudad en la que Labora', 'Teléfono Institucional', 'Extensión Telefónica',
                     'Correo Electrónico'])

    for registro in registros:
        writer.writerow([registro.numero_registro, registro.nombres_apellidos, registro.cedula,
                         registro.puesto_institucional, registro.unidad_pertenece, registro.direccion_institucional,
                         registro.ciudad_labora, registro.telefono_institucional, registro.extension_telefonica,
                         registro.correo_electronico])

    return response
