from django.shortcuts import render



def index(request):
	return render(request, 'redsocial/index.html')

def registrousuario(request):
	return render(request, 'usuario/registro.html')
	
def inicio(request):
	return render(request, 'redsocial/timeline.html')

def areadeinteres(request):
	return render(request, 'redsocial/areadeinteres.html')

def canales(request):
	return render(request, 'redsocial/canales.html')

def perfil(request):
	return render(request, 'usuario/perfil.html')

def mensaje(request):
	return render(request, 'redsocial/mensaje.html')

def notificacion(request):
	return render(request, 'redsocial/notificacion.html')

def actividad(request):
	return render(request, 'redsocial/actividad.html')

def seguidores(request):
	return render(request, 'redsocial/seguidores.html')

def seguidos(request):
	return render(request, 'redsocial/seguidos.html')

def miscanales(request):
	return render(request, 'redsocial/miscanales.html')

def misseguidos(request):
	return render(request, 'redsocial/misseguidos.html')

def misseguidores(request):
	return render(request, 'redsocial/misseguidores.html')