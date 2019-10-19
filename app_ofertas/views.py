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


def search(request):
	
	# parametro titulo
	param_titulo = request.GET.get('param_titulo','')

	# parametro order

	#	parametro	efectivo
	#	parametro	credito
	#	parametro	debito
	#	parametro	todas
	
	#	parametro delivery


	# filtrar titulo
	publicaciones = Publicacion.objects.filter(titulo__contains=param_titulo)

	#filtrar metodo pago

	#filtrar delivery

	#ordenar

	#agregar las publicaciones  rubros que entre dentro de param titulo

	contexto = {
		"publicaciones":publicaciones,
		"param": param_titulo
	}

	return render(request, "search_results.html", contexto)