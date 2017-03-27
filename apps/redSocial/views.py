from django.shortcuts import render
from django.contrib.auth import get_user_model
User = get_user_model()
from apps.redSocial.models import AreaConocimiento, Interes, Multimedia,\
								  Canal, Post, Like, Comentario, Evento, Seguimiento
from apps.redSocial.serializers import UserSerializer, AreaConocimientoSerializer, InteresSerializer,\
									   MultimediaSerializer, PostSerializer, EventoSerializer,\
									   CanalSerializer, ComentarioSerializer, LikeSerializer
#para conectarse a cumlaude
import urllib
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAdminUser
from rest_framework import viewsets, status
from rest_framework.response import Response
import json
import codecs

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny

#Set de vistas para usuario
class UserViewSet(viewsets.ModelViewSet):
	queryset = User.objects.filter(id=-1)
	serializer_class = UserSerializer
	permission_classes = (AllowAny,)

	#Devuelve la informacion de un usuario segun su pk
	def retrieve(self, request, pk):
		queryset = User.objects.get(username=pk)
		serializer = UserSerializer(queryset)
		return Response(serializer.data)

	#permite registrarse a un usuario
	def create(self, request):
		#La cookie fue asignada luego de la consulta a cumlaude
		if 'cookie' in request.session:
			cedula=request.session["cookie"]
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
					Response({'ok' : 'false', 'error' : "la contrasena no coincide"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)		
		else:
			return Response({'ok' : 'false', 'error' : "solo para egresados"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)

#Gestion de las areas de conocimiento.
class AreaConocimientoViewSet(viewsets.ModelViewSet):
	queryset = AreaConocimiento.objects.all()
	serializer_class = AreaConocimientoSerializer
	#solo un admin puede ingresar a esta seccion
	permission_classes = (IsAdminUser,)
		
class InteresViewSet(viewsets.ModelViewSet):
	queryset = Interes.objects.all()
	serializer_class = InteresSerializer
	
class MultimediaViewSet(viewsets.ModelViewSet):
	queryset = Multimedia.objects.all()
	serializer_class = MultimediaSerializer

#TimeLine publico que muestra los mensajes de cualquier usuario en la red
class PublicTimelineViewSet(viewsets.ModelViewSet):
	queryset = Post.objects.all().order_by('-creado_en')
	serializer_class = PostSerializer

	def create(self, request):
		json_data = json.loads(request.body.decode("utf-8"))#el decode "uft-8" convierte en string un byte
		user = request.user
		if Canal.objects.filter(id=1).exists():
			canal = Canal.objects.get(id=1) #El canal 1 sera por defecto el canal publico
			new_post = Post()
			new_post.contenido = json_data['contenido']
			new_post.usuario = user
			new_post.canal = canal
			new_post.estatus = json_data['estatus']
			#falta el multimedia.. ni rayos de como se hace
			new_post.save()
			return Response({'ok' : 'true'})
		else:
			return Response({'ok' : 'false', 'error' : 'No existe un canal publico'},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
		
	def update(self, request, pk):
		json_data = json.loads(request.body.decode("utf-8"))#el decode "uft-8" convierte en string un byte
		user = request.user
		if Post.objects.filter(id=pk).exists():
			post = Post.objects.get(id=pk)
			if (post.usuario.id == user.id):
				post = Post.objects.get(id=pk)
				post.contenido = json_data['contenido']
				#falta el multimedia.. ni rayos de como se hace
				post.save()
				return Response({'ok' : 'true'})
			else:
				return Response({'ok' : 'false', 'error' : 'No es propietario del post'},status=status.HTTP_403_FORBIDDEN)

		else:
			return Response({'ok' : 'false', 'error' : 'Post no encontrado'},status=status.HTTP_404_NOT_FOUND)

class PrivateTimelineViewSet(viewsets.ModelViewSet):
	queryset = Post.objects.all()
	serializer_class = PostSerializer

	def list(self, request):
		user = request.user
		seguimientos= Seguimiento.objects.filter(seguidor=user)
		seguidos_id=[user.id]
		for seguimiento in seguimientos:
			seguidos_id.append(seguimiento.seguido.id)
		print(seguidos_id)
		queryset = Post.objects.filter(usuario__id__in=seguidos_id).order_by('-creado_en')
		serializer = PostSerializer(queryset, many=True)
		return Response(serializer.data)

	def create(self, request):
		json_data = json.loads(request.body.decode("utf-8"))
		#el decode "uft-8" convierte en string un byte
		user = request.user
		if Canal.objects.filter(id=2).exists():
			canal = Canal.objects.get(id=2)
			#El canal 2 sera por defecto el canal privado
			new_post = Post()
			new_post.contenido = json_data['contenido']
			new_post.usuario = user
			new_post.canal = canal
			new_post.estatus = json_data['estatus']
			#falta el multimedia.. ni rayos de como se hace
			new_post.save()
			return Response({'ok' : 'true'})
		else:
			return Response({'ok' : 'false', 'error' : 'No existe timeline privado'},status=status.HTTP_500_INTERNAL_SERVER_ERROR)

#Esta vista administra los post que se publican en un canal que puede ver un usuario
class CanalTimelineViewSet(viewsets.ModelViewSet):
	queryset = Post.objects.all().order_by('-creado_en')
	serializer_class = PostSerializer

	def retrieve(self, request, pk):
		user = request.user
		if (Canal.objects.filter(nombre=pk).exists()):
			if(Canal.objects.filter(nombre=pk).filter(areasConocimiento__id__in=user.areasConocimiento.values_list('id', flat=True)).exists()):
				canal=Canal.objects.get(nombre=pk)
				queryset = Post.objects.filter(canal__id=canal.id).order_by('-creado_en')
				serializer = PostSerializer(queryset, many=True)
				return Response(serializer.data)
			else:
				return Response({'ok' : 'false', 'error' : 'No puede ver este canal'},status=status.HTTP_403_FORBIDDEN)
		else:
			return Response({'ok' : 'false', 'error' : 'No existe el canal'},status=status.HTTP_404_NOT_FOUND)

	def create(self, request):
		json_data = json.loads(request.body.decode("utf-8"))
		user = request.user
		#verificamos que el canal existe
		if (Canal.objects.filter(id=json_data['canal_id']).exists()):
			#verificamos que las areas de conocimiento del canal se corresponden con las del usuario
			if(Canal.objects.filter(id=json_data['canal_id']).filter(areasConocimiento__id__in=user.areasConocimiento.values_list('id', flat=True)).exists()):
				canal=Canal.objects.get(id=json_data['canal_id'])
				new_post = Post()
				new_post.contenido = json_data['contenido']
				new_post.usuario = user
				new_post.canal = canal
				new_post.estatus = '1'
				#falta el multimedia.. ni rayos de como se hace
				new_post.save()
				return Response({'ok' : 'true'})
			else:
				return Response({'ok' : 'false', 'error' : 'No puede ver este canal'},status=status.HTTP_403_FORBIDDEN)
		else:
			return Response({'ok' : 'false', 'error' : 'Canal no encontrado'},status=status.HTTP_404_NOT_FOUND)

#Muestra los mensajes publicados por un usuario en el timeline publico o privado
class UserTimelineViewSet(viewsets.ModelViewSet):
	queryset = Post.objects.filter(id=-1)
	serializer_class = PostSerializer

	def retrieve(self, request, pk):

		if (User.objects.filter(username=pk).exists()):
			user = User.objects.get(username=pk)
			#si quien solicita ver el contenido es el mismo usuario: mostrar
			if (request.user == user):
				queryset = Post.objects.filter(usuario=request.user).filter(canal__id__in=[1,2]).order_by('-creado_en')
				serializer = PostSerializer(queryset, many=True)
				return Response(serializer.data)
			#si quien solicita el contenido es seguidor del usuario: mostrar
			elif (Seguimiento.objects.filter(seguido=user).filter(seguidor=request.user).exists()):
				queryset = Post.objects.filter(usuario=user).filter(canal__id__in=[1,2]).order_by('-creado_en')
				serializer = PostSerializer(queryset, many=True)
				return Response(serializer.data)
			else:
				return Response({'ok' : 'false', 'error' : 'No sigue a este usuario'},status=status.HTTP_403_FORBIDDEN)
		else:
			return Response({'ok' : 'false', 'error' : 'Usuario no encontrado'},status=status.HTTP_404_NOT_FOUND)

#Esta clase devuelve una lista de canales en los que el usuario logueado puede participar
class CanalViewSet(viewsets.ModelViewSet):
	queryset = Canal.objects.all()
	serializer_class = CanalSerializer

	def list(self, request):
		user = request.user
		areas_usuario=[]
		for area in user.areasConocimiento.all():
			areas_usuario.append(area)
		queryset = Canal.objects.filter(areasConocimiento__in=areas_usuario)
		serializer = CanalSerializer(queryset, many=True)
		return Response(serializer.data)

class EventoViewSet(viewsets.ModelViewSet):
	queryset = Evento.objects.all()
	serializer_class = EventoSerializer
	#Ysabel

@api_view(['GET',])
@permission_classes((AllowAny,))
def CumlaudeConsulta(request, pk):
	import urllib.request
	req = urllib.request.Request('http://localhost:8001/Estudiantes/'+pk+"/")
	with urllib.request.urlopen(req) as response:
		the_page = response.read()
		json_data = json.loads(the_page.decode("utf-8"))
		if (json_data['ok']=='true'):
			request.session['cookie'] = pk
			return Response({'ok' : 'true'})
		else:
			return Response({'ok' : 'false', 'error' : error_message},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
	
class ComentarioViewSet(viewsets.ModelViewSet):
	queryset = Comentario.objects.all()
	serializer_class = ComentarioSerializer
	
	def create(self, request):

		json_data = json.loads(request.body.decode("utf-8"))
		mensaje = json_data['mensaje']
		print(mensaje)
		if (len(json_data['mensaje']) > 0):
			if (Post.objects.filter(pk=json_data['post_id']).exists()):
				post=Post.objects.get(pk=json_data['post_id'])
				print(post.canal.id)
				#si quien solicita comentar es el mismo propietario:
				if (request.user == post.usuario):
					new_comentario= Comentario()
					new_comentario.user = request.user
					new_comentario.post = post
					new_comentario.mensaje = json_data['mensaje']
					new_comentario.estatus = '1'
					new_comentario.save
					return Response({'ok' : 'true'})

				#si el post es publico
				elif (post.canal.id ==1):
					new_comentario= Comentario()
					new_comentario.usuario = request.user
					new_comentario.post = post
					new_comentario.mensaje = json_data['mensaje']
					new_comentario.estatus = "1"
					new_comentario.save()
					notify = Notificacion()
					notify.emisor=request.user
					notify.receptor=post.usuario
					notify.tipo = 'C'
					notify.visto=False
					notify.save
					return Response({'ok' : 'true'})
				
				#si el post es privado
				elif(post.canal.id ==2):
					#si quien solicita comentar es seguidor del usuario
					if (Seguimiento.objects.filter(seguido=post.usuario).filter(seguidor=request.user).exists()):
						new_comentario= Comentario()
						new_comentario.user = request.user
						new_comentario.post = post
						new_comentario.mensaje = json_data['mensaje']
						new_comentario.estatus = '1'
						new_comentario.save
						notify = Notificacion()
						notify.emisor=request.user
						notify.receptor=post.usuario
						notify.tipo = 'C'
						notify.visto=False
						notify.save
						return Response({'ok' : 'true'})
					else:
						return Response({'ok' : 'false', 'error' : 'No sigue a este usuario'},status=status.HTTP_403_FORBIDDEN)
				
				#si el usuario pertenece a el canal del post
				elif(post.canal.id > 2):
					areas_usuario=[]
					for area in request.user.areasConocimiento.all():
						areas_usuario.append(area)
					if(post.filter(canal__areasConocimiento__in=areas_usuario).exists()):
						new_comentario= Comentario()
						new_comentario.user = request.user
						new_comentario.post = post
						new_comentario.mensaje = json_data['mensaje']
						new_comentario.estatus = '1'
						new_comentario.save
						notify = Notificacion()
						notify.emisor=request.user
						notify.receptor=post.usuario
						notify.tipo = 'C'
						notify.visto=False
						notify.save
						return Response({'ok' : 'true'})
					else:
						return Response({'ok' : 'false', 'error' : 'No pertenece a este canal'},status=status.HTTP_403_FORBIDDEN)
						
				else:
					return Response({'ok' : 'false', 'error' : 'No sigue a este usuario'},status=status.HTTP_403_FORBIDDEN)
			else:
				return Response({'ok' : 'false', 'error' : 'Post no encontrado'},status=status.HTTP_404_NOT_FOUND)
		else:
			return Response({'ok' : 'false', 'error' : 'Comentario vacio'},status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class LikeViewSet(viewsets.ModelViewSet):
	queryset = Like.objects.all()
	serializer_class = LikeSerializer
	
	def create(self, request):
		json_data = json.loads(request.body.decode("utf-8"))
		if (Post.objects.filter(pk=json_data['post_id']).exists()):
			post=Post.objects.get(pk=json_data['post_id'])
			print(post.canal.id)
			#si quien solicita like es el mismo propietario:
			if (request.user == post.usuario):
				new_like= Like()
				new_like.user = request.user
				new_like.post = post
				new_like.estatus = '1'
				new_like.save
				return Response({'ok' : 'true'})

			#si el post es publico
			elif (post.canal.id ==1):
				new_like= Like()
				new_like.usuario = request.user
				new_like.post = post
				new_like.estatus = '1'
				new_like.save()
				notify = Notificacion()
				notify.emisor=request.user
				notify.receptor=post.usuario
				notify.tipo = 'L'
				notify.visto=False
				notify.save
				return Response({'ok' : 'true'})
			
			#si el post es privado
			elif(post.canal.id ==2):
				#si quien solicita like es seguidor del usuario
				if (Seguimiento.objects.filter(seguido=post.usuario).filter(seguidor=request.user).exists()):
					new_like= Like()
					new_like.user = request.user
					new_like.post = post
					new_like.estatus = '1'
					new_like.save
					notify = Notificacion()
					notify.emisor=request.user
					notify.receptor=post.usuario
					notify.tipo = 'L'
					notify.visto=False
					notify.save
					return Response({'ok' : 'true'})
				else:
					return Response({'ok' : 'false', 'error' : 'No sigue a este usuario'},status=status.HTTP_403_FORBIDDEN)
			
			#si el usuario pertenece a el canal del post
			elif(post.canal.id > 2):
				areas_usuario=[]
				for area in request.user.areasConocimiento.all():
					areas_usuario.append(area)
				if(post.filter(canal__areasConocimiento__in=areas_usuario).exists()):
					new_like= Like()
					new_like.user = request.user
					new_like.post = post
					new_like.estatus = '1'
					new_like.save
					notify = Notificacion()
					notify.emisor=request.user
					notify.receptor=post.usuario
					notify.tipo = 'L'
					notify.visto=False
					notify.save
					return Response({'ok' : 'true'})
				else:
					return Response({'ok' : 'false', 'error' : 'No pertenece a este canal'},status=status.HTTP_403_FORBIDDEN)
					
			else:
				return Response({'ok' : 'false', 'error' : 'No sigue a este usuario'},status=status.HTTP_403_FORBIDDEN)
		else:
			return Response({'ok' : 'false', 'error' : 'Post no encontrado'},status=status.HTTP_404_NOT_FOUND)

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
		notify = Notificacion()
		notify.emisor=user
		notify.receptor=seguido
		notify.tipo = 'S'
		notify.visto=False
		notify.save
		return Response({'ok' : 'true'})
	
@api_view(['GET',])
def Seguidores(request,pk):
	user = User.objects.get(id=pk)
	seguimientos= Seguimiento.objects.filter(seguido=user)
	seguidores_id=[]
	for seguimiento in seguimientos:
		seguidores_id.append(seguimiento.seguidor.id)
	print(seguidores_id)
	queryset=User.objects.filter(id__in=seguidores_id)
	serializer = UserSerializer(queryset, many=True)
	return Response(serializer.data)
	
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

