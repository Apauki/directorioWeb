from django.shortcuts import render, redirect
from .models import Registro
from .forms import RegistroForm

def lista_registros(request):
    registros = Registro.objects.all()
    return render(request, 'lista_registros.html', {'registros': registros})

def agregar_registro(request):
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('agregar_registro')
    else:
        form = RegistroForm()
    return render(request, 'agregar_registro.html', {'form': form})

def editar_registro(request, numero_registro):
    registro = Registro.objects.get(numero_registro=numero_registro)
    if request.method == 'POST':
        form = RegistroForm(request.POST, instance=registro)
        if form.is_valid():
            form.save()
            return redirect('lista_registros')
    else:
        form = RegistroForm(instance=registro)
    return render(request, 'editar_registro.html', {'form': form, 'registro': registro})

def eliminar_registro(request, numero_registro):
    registro = Registro.objects.get(numero_registro=numero_registro)
    registro.delete()
    return redirect('lista_registros')