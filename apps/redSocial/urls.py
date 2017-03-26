from django.conf.urls import include, url
from rest_framework import routers
from apps.redSocial import views



router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'areas', views.AreaConocimientoViewSet)
router.register(r'intereses',views.InteresViewSet)
router.register(r'multimedia',views.MultimediaViewSet)
router.register(r'evento',views.EventoViewSet)
router.register(r'public-timeline',views.PublicTimelineViewSet)
router.register(r'private-timeline',views.PrivateTimelineViewSet)
router.register(r'canal-timeline',views.CanalTimelineViewSet)
router.register(r'canales',views.CanalViewSet)
router.register(r'user-timeline',views.UserTimelineViewSet)
router.register(r'comentarios',views.ComentarioViewSet)
router.register(r'like',views.LikeViewSet)
router.register(r'post-comentarios',views.PostComentariosViewSet)

urlpatterns = [ 
    url(r'^entities/', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^rest-auth/', include('rest_auth.urls')),
    url(r'^rest-auth/registration/', include('rest_auth.registration.urls')),
    url(r'^entities/cumlaude/(?P<pk>\d+)/', views.CumlaudeConsulta, name= 'cumlaude'),
    url(r'^entities/seguir/$', views.Seguir, name= 'seguir'),
    url(r'^entities/seguidores/(?P<pk>\d+)/', views.Seguidores, name= 'seguidores'),
    url(r'^entities/seguidos/(?P<pk>\d+)/', views.Seguidos, name= 'seguidos'),
]

