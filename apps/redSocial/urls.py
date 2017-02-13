

#aun no se usara de esta forma
from django.conf.urls import url, include
from rest_framework import routers
from apps.redSocial import views
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

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


urlpatterns = [ 
    url(r'^', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^admin/', admin.site.urls),
    url(r'^rest-auth/', include('rest_auth.urls')),
    url(r'^rest-auth/registration/', include('rest_auth.registration.urls')),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
