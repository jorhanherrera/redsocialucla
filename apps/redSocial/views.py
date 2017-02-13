from django.shortcuts import render
from django.contrib.auth import get_user_model
User = get_user_model()
from apps.redSocial.models import AreaConocimiento, Interes, Multimedia,\
								  Canal, Post, Like, Comentario, Evento, Seguimiento
from apps.redSocial.serializers import UserSerializer, AreaConocimientoSerializer, InteresSerializer,\
									   MultimediaSerializer, PostSerializer, EventoSerializer,\
									   CanalSerializer, ComentarioSerializer
#para conectarse a cumlaude
import urllib
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAdminUser
from rest_framework import viewsets, status
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

	def create(self, request):
		#print(request.session['cookie'])
		if 'cookie' in request.session:
			cedula=request.session["cookie"]
			print(request.session['cookie'])
			if User.objects.filter(cedula=cedula).exists():
				return Response({'ok' : 'false', 'error' : "ya esta registrado"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
			else:
				json_data = json.loads(request.body.decode("utf-8"))
				password1=json_data['password1']
				password2=json_data['password2']
				if (password1==password2 and password1!= ""):
					user = User()
					user.username = json_data['username']
					user.email = json_data['email']
					user.set_password(password1)
					user.cedula = cedula
					user.save()
					return Response({'ok' : 'true'})
				else:
					Response({'ok' : 'false', 'error' : "contrasena no coincide"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)		
		else:
			return Response({'ok' : 'false', 'error' : "solo para egresados"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class AreaConocimientoViewSet(viewsets.ModelViewSet):
	queryset = AreaConocimiento.objects.all()
	serializer_class = AreaConocimientoSerializer
	permission_classes = (IsAdminUser,)
		
class InteresViewSet(viewsets.ModelViewSet):
	queryset = Interes.objects.all()
	serializer_class = InteresSerializer
	
class MultimediaViewSet(viewsets.ModelViewSet):
	queryset = Multimedia.objects.all()
	serializer_class = MultimediaSerializer


class PublicTimelineViewSet(viewsets.ModelViewSet):
	queryset = Post.objects.all().order_by('-creado_en')
	serializer_class = PostSerializer

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
	def update(self, request, pk):
		json_data = json.loads(request.body.decode("utf-8"))#el decode "uft-8" convierte en string un byte
		user = request.user
		canal = Canal.objects.get(id=1) #El canal 1 sera por defecto el canal publico
		if(canal != None):
			post = Post.objects.get(id=pk)
			post.contenido = json_data['contenido']
			#falta el multimedia.. ni rayos de como se hace
			post.save()
			return Response({'ok' : 'true'})
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

class UserTimelineViewSet(viewsets.ModelViewSet):
	queryset = Post.objects.all()
	serializer_class = PostSerializer

	def retrieve(self, request, pk):
		user = User.objects.filter(username=pk)
		queryset = Post.objects.filter(usuario=user).filter(canal__id=1).order_by('-creado_en')
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

@api_view(['GET','POST',])
def CumlaudeConsulta(request, pk):
	if request.method =='GET':
		import urllib.request
		req = urllib.request.Request('http://127.0.0.1:8001/Estudiantes/'+pk+"/")
		with urllib.request.urlopen(req) as response:
			the_page = response.read()
			json_data = json.loads(the_page.decode("utf-8"))
			if (json_data['ok']=='true'):
				request.session['cookie'] = pk
				return Response({'ok' : 'true'})
			else:
				return Response({'ok' : 'false', 'error' : error_message},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
	else:
		return Response({'ok' : 'false', 'error' : error_message},status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class ComentarioViewSet(viewsets.ModelViewSet):
	queryset = Comentario.objects.all()
	serializer_class = ComentarioSerializer

class PostComentariosViewSet(viewsets.ModelViewSet):
	queryset = Comentario.objects.all()
	serializer_class = ComentarioSerializer

	def retrieve(self, request, pk):
		queryset = Comentario.objects.filter(post__id=pk).order_by('-fecha')
		serializer = ComentarioSerializer(queryset, many=True)
		return Response(serializer.data)

@api_view(['GET','POST',])
def CompartirTwitter(request, pk):
	if request.method =='GET':
		import urllib.request
		req = urllib.request.Request('https://twitter.com/home?status=Prueba%20de%20app.%20Contenido%20compartido%20desde%20Exodo%2C%20la%20Red%20Social%20para%20egresados%20de%20la%20UCLA.%20%23Exodo%20%23UCLA%20%23LAB3/')
		with urllib.request.urlopen(req) as response:
			the_page = response.read()
			json_data = json.loads(the_page.decode("utf-8"))
			if (json_data['ok']=='true'):
				request.session['cookie'] = pk
				return Response({'ok' : 'true'})
			else:
				return Response({'ok' : 'false', 'error' : error_message},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
	else:
		return Response({'ok' : 'false', 'error' : error_message},status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST',])
def Seguir(request):
	if request.method =='POST':
		json_data = json.loads(request.body.decode("utf-8"))
		user = request.user
		print(json_data)
		seguido_id=json_data['seguido_id']
		if (Seguimiento.objects.filter(seguidor__id=user.id).filter(seguido__id=seguido_id).exists()):
			return Response({'ok' : 'false', 'error' : 'Ya se ha seguido a este usuario'},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
		else:
			seguido = User.objects.get(id=seguido_id)
			seguimiento = Seguimiento()
			seguimiento.seguidor=user
			seguimiento.seguido=seguido
			seguimiento.save()
			return Response({'ok' : 'true'})
	else:
		return Response({'ok' : 'false', 'error' : 'Solo metodo post'},status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET',])
def Seguidores(request,pk):
	if request.method =='GET':
		user = User.objects.get(id=pk)
		seguimientos= Seguimiento.objects.filter(seguido=user)
		seguidores_id=[]
		for seguimiento in seguimientos:
			seguidores_id.append(seguimiento.seguidor.id)
		print(seguidores_id)
		queryset=User.objects.filter(id__in=seguidores_id)
		serializer = UserSerializer(queryset, many=True)
		return Response(serializer.data)
	else:
		return Response({'ok' : 'false', 'error' : 'Solo metodo get'},status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET',])
def Seguidos(request,pk):
	user = User.objects.get(id=pk)
	seguimientos= Seguimiento.objects.filter(seguidor=user)
	seguidos_id=[]
	for seguimiento in seguimientos:
		seguidos_id.append(seguimiento.seguido.id)
	print(seguidos_id)
	queryset=User.objects.filter(id__in=seguidos_id)
	serializer = UserSerializer(queryset, many=True)
	return Response(serializer.data)