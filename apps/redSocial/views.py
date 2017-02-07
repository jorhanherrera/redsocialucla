from django.shortcuts import render
from django.contrib.auth.models import User
from apps.redSocial.models import Perfil, AreaConocimiento, Interes, Multimedia, Canal, Post, Like, Comentario, Evento
from rest_framework import viewsets
from apps.redSocial.serializers import UserSerializer, AreaConocimientoSerializer, InteresSerializer, MultimediaSerializer, PostSerializer, PerfilSerializer, EventoSerializer

class UserViewSet(viewsets.ModelViewSet):
	queryset = User.objects.all().order_by('-date_joined')
	serializer_class = UserSerializer

class AreaConocimientoViewSet(viewsets.ModelViewSet):
	queryset = AreaConocimiento.objects.all()
	serializer_class = AreaConocimientoSerializer
	
class InteresViewSet(viewsets.ModelViewSet):
	queryset = Interes.objects.all()
	serializer_class = InteresSerializer
	
class MultimediaViewSet(viewsets.ModelViewSet):
	queryset = Multimedia.objects.all()
	serializer_class = MultimediaSerializer

class PostViewSet(viewsets.ModelViewSet):
	queryset = Post.objects.all()
	serializer_class = PostSerializer

class PerfilViewSet(viewsets.ModelViewSet):
	queryset = Perfil.objects.all()
	serializer_class = PerfilSerializer

class EventoViewSet(viewsets.ModelViewSet):
	queryset = Evento.objects.all()
	serializer_class = EventoSerializer
