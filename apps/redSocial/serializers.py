from rest_framework.serializers import ModelSerializer
#from django.contrib.auth.models import User
from apps.redSocial.models import AreaConocimiento, Interes,\
								  Multimedia, Canal, Post, Like,\
								  Comentario, Evento, Notificacion
from rest_framework import serializers
from django.contrib.auth import get_user_model
User = get_user_model()

class UserSerializer(ModelSerializer):
	class Meta:
		model = User
		fields = ('username','first_name','last_name','foto','last_login','email','is_superuser','is_active')

class PropietarioSerializer(ModelSerializer):
	class Meta:
		model=User
		fields=('username', 'foto', 'is_active')

class CommentSerializer(ModelSerializer):
	usuario=PropietarioSerializer()
	class Meta:
		model=Comentario
		fields=('fecha', 'usuario', 'mensaje' )

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
	usuario=PropietarioSerializer(many=False, read_only=True)
	areasConocimiento=AreaConocimientoSerializer(many=True, read_only=True)
	class Meta:
		model = Canal
		fields = ('usuario', 'areasConocimiento', 'nombre', 'descripcion', 'fecha', 'logo', 'estatus')

class EventoSerializer(ModelSerializer):
	propietario=PropietarioSerializer()
	class Meta:
		model = Evento
		fields = ('titulo', 'descripcion', 'fecha', 'logo', 'propietario', 'estatus')

class PostSerializer(ModelSerializer):
	usuario = PropietarioSerializer()
	canal = CanalSerializer(many=False, read_only=True)
	multimedia = MultimediaSerializer()
	comentarios=CommentSerializer(many=True, read_only=True)
	class Meta:
		model = Post
		fields = ('id','contenido', 'canal', 'usuario', 'multimedia', 'creado_en', 'estatus', 'comentarios', 'likes',)

class LikeSerializer(ModelSerializer):
	usuario = PropietarioSerializer()
	class Meta:
		model = Like
		fields = ('usuario', 'post', 'fecha', 'estatus')

class ComentarioSerializer(ModelSerializer):
	usuario = PropietarioSerializer()
	class Meta:
		model = Comentario
		fields = ('usuario', 'post', 'mensaje', 'fecha', 'estatus')

class NotificacionSerializer(ModelSerializer):
	emisor = PropietarioSerializer()
	receptor = PropietarioSerializer()
	class Meta:
		model = Notificacion
		fields = ('tipo', 'creado_en', 'visto')
