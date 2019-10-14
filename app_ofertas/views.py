from django.shortcuts import render
from app_ofertas.models import Publicacion,Rubro

# Create your views here.
def hometest(request):
	return render(request, 'esquema.html',{})

def index(request):
	#Obtener 9 ofertas recientes (mando todas mientras CORREGIR )
	recientes=Publicacion.objects.all()
	#últimas 9
	#recientes=Publicacion.objects.order_by('-id')[:9]
	#Obtener las categorías
	categorias = Rubro.objects.all()

	return render(request,'home.html',{'recientes':recientes, 'categorias':categorias})