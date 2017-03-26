from django.db import models
#from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser

class AreaConocimiento(models.Model):
	descripcion = models.CharField(max_length=25)
	estatus = models.CharField(max_length=1)

	def __str__(self):
		return '{}'.format(self.descripcion)

class Interes(models.Model):
	descripcion = models.CharField(max_length=25)
	estatus = models.CharField(max_length=1)

	def __str__(self):
		return '{}'.format(self.descripcion)

class Usuario(AbstractUser):
	birth_date = models.DateField(null=True, blank=True)
	bio = models.DateField(null=True, blank=True)
	sexo = models.CharField(max_length=1, blank=True)
	foto = models.ImageField(blank=True, null=True)
	intereses = models.ManyToManyField(Interes)
	areasConocimiento = models.ManyToManyField(AreaConocimiento)
	cedula = models.CharField(max_length=10, blank=False)

class Seguimiento(models.Model):
	seguidor = models.ForeignKey(Usuario, editable=True,
                                    related_name='seguidor')
	seguido = models.ForeignKey(Usuario, editable=True,
                                    related_name='seguido')

class Canal(models.Model):
	usuario = models.ForeignKey(Usuario,on_delete=models.CASCADE)
	areasConocimiento = models.ManyToManyField(AreaConocimiento)
	nombre = models.CharField(max_length=25, unique=True)
	descripcion = models.TextField()
	fecha = models.DateTimeField(auto_now_add=True)
	logo = models.ImageField(null=True, blank=True)
	estatus = models.CharField(max_length=1)

	def __str__(self):
		return '{}'.format(self.nombre)

class Evento(models.Model):
	titulo = models.CharField(max_length=25)
	descripcion = models.TextField()
	fecha = models.DateTimeField()
	imagen = models.ImageField(null=True)
	propietario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
	estatus = models.CharField(max_length=1)

	def __str__(self):
		return '{}'.format(self.titulo)

class Multimedia(models.Model):
	recurso = models.FileField(blank=True, null=True)
	tipo = models.CharField(max_length=1, blank=True, null=True)

class Post(models.Model):
	contenido = models.TextField()
	canal = models.ForeignKey(Canal,on_delete=models.CASCADE)
	usuario = models.ForeignKey(Usuario,on_delete=models.CASCADE)
	creado_en = models.DateTimeField(auto_now_add=True)
	estatus = models.CharField(max_length=1)
	multimedia = models.OneToOneField(Multimedia,
						 on_delete=models.CASCADE,
						  blank=True, null=True)

class Like(models.Model):
	usuario = models.ForeignKey(Usuario,on_delete=models.CASCADE)
	post = models.ForeignKey(Post, editable=True, related_name='likes')
	fecha = models.DateTimeField(auto_now_add=True)
	estatus = models.CharField(max_length=1)

class Comentario(models.Model):
	usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
	post = models.ForeignKey(Post, editable=True, related_name='comentarios')
	mensaje = models.TextField(blank=True, null=True)
	fecha = models.DateTimeField(auto_now_add=True)
	estatus = models.CharField(max_length=1)

class Notificacion(models.Model):
	emisor = models.ForeignKey(Usuario, on_delete=models.CASCADE,editable=True, related_name='emisores')
	receptor = models.ForeignKey(Usuario, on_delete=models.CASCADE, editable=True, related_name='receptores')
	tipo = models.CharField(max_length=1)
	visto = models.BooleanField()
	creado_en = models.DateTimeField(auto_now_add=True)