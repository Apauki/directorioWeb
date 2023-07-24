from django.db import models
from django.contrib.auth.models import AbstractUser

class Registro(models.Model):
    numero_registro = models.IntegerField(unique=True)
    nombres_apellidos = models.CharField(max_length=255)
    cedula = models.CharField(max_length=10)
    puesto_institucional = models.CharField(max_length=255)
    unidad_pertenece = models.CharField(max_length=255)
    direccion_institucional = models.CharField(max_length=255)
    ciudad_labora = models.CharField(max_length=255)
    telefono_institucional = models.CharField(max_length=255)
    extension_telefonica = models.CharField(max_length=255)
    correo_electronico = models.EmailField()

    def save(self, *args, **kwargs):
        if not self.pk:
            # Nuevo registro, asignar número automático
            ultimo_registro = Registro.objects.order_by('-numero_registro').first()
            if ultimo_registro:
                self.numero_registro = ultimo_registro.numero_registro + 1
            else:
                self.numero_registro = 1
        super().save(*args, **kwargs)

    # Actualizar número de registro al eliminar
    @staticmethod
    def update_numeros_registro():
        registros = Registro.objects.order_by('id')
        for index, registro in enumerate(registros, start=1):
            registro.numero_registro = index
            registro.save(update_fields=['numero_registro'])

    def __str__(self):
        return self.nombres_apellidos

'''
class User(AbstractUser):
    email = models.EmailField(unique=True, max_length=254)
    
    # No es necesario definir un UserManager personalizado

    def __str__(self):
        return self.email
'''