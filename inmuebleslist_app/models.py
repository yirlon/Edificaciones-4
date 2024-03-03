from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from user_app.models import Account


class Empresa(models.Model):
    nombre = models.CharField(max_length=250)
    website = models.URLField(max_length=250)  
    active = models.BooleanField(default=True) 

    def __str__(self): 
        return self.nombre
    

class Inmuebles(models.Model):
    direccion = models.CharField(max_length=250, null=True)
    pais = models.CharField(max_length=150, null=True)
    descripcion = models.CharField(max_length=500)
    imagen = models.CharField(max_length=900)
    avg_calificacion = models.FloatField(default=0)
    number_calificacion = models.IntegerField(default=0)
    active = models.BooleanField(default=True)                      
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, related_name='edificacionlist')                                  
    created = models.DateTimeField(auto_now_add=True)
   
    def __str__(self):
        return self.direccion

class Comment(models.Model):
    calificacion = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])  
    inmueble = models.ForeignKey(Inmuebles, related_name='comments', on_delete=models.CASCADE, null=True)
    comentario_user = models.ForeignKey(Account, on_delete=models.CASCADE) 
    nombre_comentario = models.CharField(max_length=200)
    comentario = models.TextField()
    active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True, null=True)
    update = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return str(self.comentario_user)
    