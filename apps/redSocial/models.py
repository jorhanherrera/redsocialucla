from django.db import models

# Create your models here.

class AreaConocimiento(models.Model):
	descripcion = models.CharField(max_length=25)
	estatus = models.CharField(max_length=1)

class Interes(models.Model):
	descripcion = models.CharField(max_length=25)
	estatus = models.CharField(max_length=1)

class Multimedia(models.Model):
	recurso = models.FileField()
	tipo = models.CharField(max_length=1)

class Usuario(models.Model):
	cedula = models.CharField(max_length=15, primary_key=True)
	nombre = models.CharField(max_length=25)
	apellido = models.CharField(max_length=25)
	correo = models.EmailField(unique=True)
	fechaNacimiento = models.DateField()
	sexo = models.CharField(max_length=1)
	password = models.TextField(models.SET_NULL,blank=True,null=True)
	foto = models.ImageField()
	rol = models.CharField(max_length=1)
	estatus = models.CharField(max_length=1)
	areasConocimiento = models.ManyToManyField(AreaConocimiento)
	intereses = models.ManyToManyField(Interes)

class Canal(models.Model):
	usuario = models.ForeignKey(Usuario,on_delete=models.CASCADE)
	areasConocimiento = models.ManyToManyField(AreaConocimiento)
	nombre = models.CharField(max_length=25)
	descripcion = models.TextField()
	fecha = models.DateTimeField()
	logo = models.ImageField()
	estatus = models.CharField(max_length=1)

class Evento(models.Model):
	titulo = models.CharField(max_length=25)
	descripcion = models.TextField()
	fecha = models.DateTimeField()
	logo = models.ImageField()
	propietario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
	estatus = models.CharField(max_length=1)

class Post(models.Model):
	titulo = models.CharField(max_length=50)
	canal = models.ForeignKey(Canal,on_delete=models.CASCADE)
	usuario = models.ForeignKey(Usuario,on_delete=models.CASCADE)
	multimedia = models.ForeignKey(Multimedia,on_delete=models.CASCADE)
	creado_en = models.DateTimeField(auto_now_add=True)
	estatus = models.CharField(max_length=1)

class Like(models.Model):
	usuario = models.ForeignKey(Usuario,on_delete=models.CASCADE)
	post = models.ForeignKey(Post,on_delete=models.CASCADE)
	fecha = models.DateTimeField(auto_now_add=True)
	estatus = models.CharField(max_length=1)

class Comentario(models.Model):
	usuario = models.ForeignKey(Usuario,on_delete=models.CASCADE)
	post = models.ForeignKey(Post,on_delete=models.CASCADE)
	mensaje = models.TextField()
	fecha = models.DateTimeField(auto_now_add=True)
	estatus = models.CharField(max_length=1)