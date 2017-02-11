from django.shortcuts import render
from django.contrib.auth import get_user_model
User = get_user_model()
from apps.redSocial.models import AreaConocimiento, Interes, Multimedia,\
								  Canal, Post, Like, Comentario, Evento, Seguimiento
from rest_framework import viewsets
from apps.redSocial.serializers import UserSerializer, AreaConocimientoSerializer, InteresSerializer,\
									   MultimediaSerializer, PostSerializer, EventoSerializer, CanalSerializer
from rest_framework.response import Response
import json
import codecs

class UserViewSet(viewsets.ModelViewSet):
	queryset = User.objects.all().order_by('-date_joined')
	serializer_class = UserSerializer

	def list(self, request):
		#user = request.user
		queryset = User.objects.all()
		serializer = UserSerializer(queryset, many=True)
		return Response(serializer.data)

	def retrieve(self, request, pk):
		queryset = User.objects.get(username=pk)
		print(queryset.username)
		serializer = UserSerializer(queryset)
		return Response(serializer.data)

class AreaConocimientoViewSet(viewsets.ModelViewSet):
	queryset = AreaConocimiento.objects.all()
	serializer_class = AreaConocimientoSerializer
	
class InteresViewSet(viewsets.ModelViewSet):
	queryset = Interes.objects.all()
	serializer_class = InteresSerializer
	
class MultimediaViewSet(viewsets.ModelViewSet):
	queryset = Multimedia.objects.all()
	serializer_class = MultimediaSerializer


class PublicTimelineViewSet(viewsets.ModelViewSet):
	queryset = Post.objects.all()
	serializer_class = PostSerializer

	def list(self, request):
		user = request.user
		queryset = Post.objects.all().order_by('-creado_en')
		serializer = PostSerializer(queryset, many=True)
		return Response(serializer.data)

	def create(self, request):
		json_data = json.loads(request.body.decode("utf-8"))#el decode "uft-8" convierte en string un byte
		user = request.user
		if (user != None):
			canal = Canal.objects.get(id=1) #El canal 1 sera por defecto el canal publico
			if(canal != None):
				new_post = Post()
				new_post.contenido = json_data['contenido']
				new_post.usuario = user
				new_post.canal = canal
				new_post.estatus = json_data['estatus']
				#falta el multimedia.. ni rayos de como se hace
				new_post.save()
				return Response({'ok' : 'true'})
			else:
				return Response({'ok' : 'false', 'error' : error_message},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
		else:
			return Response({'ok' : 'false', 'error' : error_message},status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class PrivateTimelineViewSet(viewsets.ModelViewSet):
	queryset = Post.objects.all()
	serializer_class = PostSerializer

	def list(self, request):
		user = request.user
		seguimientos= Seguimiento.objects.filter(seguidor=user)
		xs=[user.id]
		for seguimiento in seguimientos:
			xs.append(seguimiento.seguido.id)
		print(xs)
		queryset = Post.objects.filter(usuario__id__in=xs).order_by('-creado_en')
		serializer = PostSerializer(queryset, many=True)
		return Response(serializer.data)

	def create(self, request):
		json_data = json.loads(request.body.decode("utf-8"))
		#el decode "uft-8" convierte en string un byte
		user = request.user
		if (user != None):
			canal = Canal.objects.get(id=2)
			#El canal 2 sera por defecto el canal privado
			if(canal != None):
				new_post = Post()
				new_post.contenido = json_data['contenido']
				new_post.usuario = user
				new_post.canal = canal
				new_post.estatus = json_data['estatus']
				#falta el multimedia.. ni rayos de como se hace
				new_post.save()
				return Response({'ok' : 'true'})
			else:
				return Response({'ok' : 'false', 'error' : error_message},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
		else:
			return Response({'ok' : 'false', 'error' : error_message},status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class CanalTimelineViewSet(viewsets.ModelViewSet):
	queryset = Post.objects.all()
	serializer_class = PostSerializer

	def retrieve(self, request, pk):
		user = request.user
		canal_id = pk
		queryset = Post.objects.filter(canal__id=canal_id).order_by('-creado_en')
		serializer = PostSerializer(queryset, many=True)
		return Response(serializer.data)

	def create(self, request):
		json_data = json.loads(request.body.decode("utf-8"))
		#el decode "uft-8" convierte en string un byte
		user = request.user
		if (user != None):
			canal = Canal.objects.get(json_data['canal_id']) 
			if(canal != None):
				new_post = Post()
				new_post.contenido = json_data['contenido']
				new_post.usuario = user
				new_post.canal = canal
				new_post.estatus = json_data['estatus']
				#falta el multimedia.. ni rayos de como se hace
				new_post.save()
				return Response({'ok' : 'true'})
			else:
				return Response({'ok' : 'false', 'error' : error_message},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
		else:
			return Response({'ok' : 'false', 'error' : error_message},status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class CanalViewSet(viewsets.ModelViewSet):
	queryset = Canal.objects.all()
	serializer_class = CanalSerializer

	def list(self, request):
		user = request.user
		print(user.username)
		areas_usuario=[]
		for area in user.areasConocimiento.all():
			areas_usuario.append(area)
		
		print(areas_usuario)
		queryset = Canal.objects.filter(areasConocimiento__in=areas_usuario)
		serializer = CanalSerializer(queryset, many=True)
		return Response(serializer.data)

class EventoViewSet(viewsets.ModelViewSet):
	queryset = Evento.objects.all()
	serializer_class = EventoSerializer