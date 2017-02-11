from django.contrib import admin

# Register your models here.

from apps.redSocial.models import AreaConocimiento, Interes, Multimedia, Canal, Post, Like, Comentario, Evento, Usuario, Seguimiento

admin.site.register(Usuario)
admin.site.register(AreaConocimiento)
admin.site.register(Interes)
admin.site.register(Multimedia)
admin.site.register(Canal)
admin.site.register(Post)
admin.site.register(Like)
admin.site.register(Comentario)
admin.site.register(Evento)
admin.site.register(Seguimiento)