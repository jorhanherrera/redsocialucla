from rest_framework.serializers import ModelSerializer
#from django.contrib.auth.models import User
from apps.redSocial.models import AreaConocimiento, Interes, Multimedia, Canal, Post, Like, Comentario, Evento
from rest_framework import serializers
from django.contrib.auth import get_user_model
User = get_user_model()

class UserSerializer(ModelSerializer):
	class Meta:
		model = User
		fields = ('username','first_name','last_name','last_login','email','is_superuser','is_active')

class PropietarioSerializer(ModelSerializer):
	class Meta:
		model=User
		fields=('username', 'is_active')

class AreaConocimientoSerializer(ModelSerializer):
	class Meta:
		model = AreaConocimiento
		fields = ('descripcion','estatus')

class InteresSerializer(ModelSerializer):
	class Meta:
		model = Interes
		fields = ('descripcion', 'estatus')

class MultimediaSerializer(ModelSerializer):
	class Meta:
		model = Multimedia
		fields = ('recurso', 'tipo')

class CanalSerializer(ModelSerializer):
	usuario=serializers.PrimaryKeyRelatedField(many=False, queryset= User.objects.all())
	areasConocimiento=serializers.PrimaryKeyRelatedField(many=True, queryset= AreaConocimiento.objects.all())
	class Meta:
		model = Canal
		fields = ('usuario', 'areasConocimiento', 'nombre', 'descripcion', 'fecha', 'logo', 'estatus')

class EventoSerializer(ModelSerializer):
	propietario=PropietarioSerializer()
	class Meta:
		model = Evento
		fields = ('titulo', 'descripcion', 'fecha', 'logo', 'propietario', 'estatus')

class PostSerializer(ModelSerializer):
	usuario = serializers.PrimaryKeyRelatedField(many=False, queryset= User.objects.all())
	canal = serializers.PrimaryKeyRelatedField(many=False, queryset= Canal.objects.all())
	multimedia = MultimediaSerializer()
	class Meta:
		model = Post
		fields = ('contenido', 'canal', 'usuario', 'multimedia', 'creado_en', 'estatus', 'comentarios', 'likes')

class LikeSerializer(ModelSerializer):
	propietario = PropietarioSerializer()
	post = PostSerializer()
	class Meta:
		model = Like
		fields = ('propietario', 'post', 'fecha', 'estatus')

class ComentarioSerializer(ModelSerializer):
	propietario = PropietarioSerializer()
	post = PostSerializer()
	class Meta:
		model = Like
		fields = ('propietario', 'post', 'mensaje', 'fecha', 'estatus')
