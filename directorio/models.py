from django.db import models

# Create your models here.

class Registro(models.Model):
    numero_registro = models.AutoField(primary_key=True)
    nombres_apellidos = models.CharField(max_length=255)
    puesto_institucional = models.CharField(max_length=255)
    unidad_pertenece = models.CharField(max_length=255)
    direccion_institucional = models.CharField(max_length=255)
    ciudad_labora = models.CharField(max_length=255)
    telefono_institucional = models.CharField(max_length=255)
    extension_telefonica = models.CharField(max_length=255)
    correo_electronico = models.EmailField()

    def __str__(self):
        return self.nombres_apellidos