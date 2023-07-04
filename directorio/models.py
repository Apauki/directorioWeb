from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models

# Create your models here.

class Registro(models.Model):
    numero_registro = models.IntegerField(unique=True)
    nombres_apellidos = models.CharField(max_length=255)
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

    def __str__(self):
        return self.nombres_apellidos
    
class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('El correo electrónico es obligatorio')
        
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True, max_length=254)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'

    def __str__(self):
        return self.emai