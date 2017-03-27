from django.conf.urls import url, include
from rest_framework import routers
from apps.consumir import views
from django.contrib import admin


urlpatterns = [
    url(r'^index/',views.index),
    url(r'^inicio/',views.inicio),
    url(r'^registro/',views.registrousuario),
    url(r'^areadeinteres/',views.areadeinteres),
    url(r'^canales/',views.canales),
    url(r'^perfil/',views.perfil),
    url(r'^mensaje/',views.mensaje),
    url(r'^notificacion/',views.notificacion),
    url(r'^actividad/',views.actividad),
    url(r'^seguidores/',views.seguidores),
    url(r'^seguidos/',views.seguidos),
    url(r'^miscanales/',views.miscanales),
    url(r'^misseguidos/',views.misseguidos),
    url(r'^misseguidores/',views.misseguidores),
]