from django.shortcuts import render
from app_ofertas.models import Publicacion,Rubro, Local
from app_ofertas.forms import LocalForm, PublicacionForm

# Create your views here.
def hometest(request):
	return render(request, 'esquema.html',{})

def index(request):
	#Obtener 9 ofertas recientes (mando todas mientras CORREGIR )
	recientes=Publicacion.objects.all()
	#últimas 9
	#recientes=Publicacion.objects.order_by('-id')[:9]
	#Obtener las categorías
	categorias = Rubro.objects.all().order_by('nombre')

	return render(request,'home.html',{'recientes':recientes, 'categorias':categorias})


#Manda a search_result, con las publicaciones y parametros de la busqueda
def search(request):	
	# parametro titulo
	param_titulo = request.GET.get('param_titulo','')
	param_payment = request.GET.get('param_payment','')
	param_delivery = request.GET.get('param_delivery','')
	param_orden =request.GET.get('param_orden','')

	# filtrar titulo
	publicaciones = Publicacion.objects.filter(titulo__contains=param_titulo)

	#filtrar metodo pago
	if (param_payment=="PAY_CASH"):
		print(param_payment)
	elif (param_payment=="PAY_DEBIT"):
		print(param_payment)
	elif (param_payment =="PAY_CREDIT"):
		print(param_payment)
	else:
		print(param_payment)
	
	#filtrar delivery
	if (param_delivery=="SI"):
		print(param_delivery)
	elif (param_delivery=="NO"):
		print(param_delivery)
	else:
		print(param_delivery)

	#agregar las publicaciones  rubros que entre dentro de param titulo
	#

	#ordenar
	if (param_orden == "1"):
		#de menor a mayor precio
		publicaciones = publicaciones.order_by('precio_regular')
	elif (param_orden == "2"):
		#de mayor a menor precio
		publicaciones = publicaciones.order_by('-precio_regular')
	else:
		#por abecedario
		publicaciones = publicaciones.order_by('titulo')

	#preparar contexto para el template
	contexto = {
		"publicaciones":publicaciones,
		"param_titulo": param_titulo,
		"param_payment": param_payment,
		"param_delivery": param_delivery,
		"param_orden": param_orden
	}

	return render(request, "search/search_results.html", contexto)
#fin Search()

def agregar_local(request):
	if request.method == 'POST':
		form = LocalForm(request.POST)
		if form.is_valid():
			local = form.save()

			return redirect('local')

	else:
		form = LocalForm()
		return render(request, 'local/alta_local.html',{'form':form})

def agregar_publicacion(request):
	if request.method == 'POST':
		form = PublicacionForm(request.POST)
		if form.is_valid():
			publicacion = form.save()

	else:
		form = PublicacionForm()
		return render(request, 'publicacion/agregar_publicacion.html',{'form':form})



def favoritos(request):
	#lugares favoritos
	contexto = {

	}
	return render(request, "favoritos.html", contexto)

def tendencia(request):
	#obtener 12 publicaciones mas populares
	contexto = {

	}
	return render(request, "tendencia.html", contexto)

def intereses(request):
	#publicaciones rubros favoritos
	contexto = {

	}
	return render(request, "intereses.html", contexto)

def ver_publicacion(request,id):
	try:
		pub=Publicacion.objects.get(pk=id)
	except Publicacion.DoesNotExist:
		raise Http404("Esta oferta no se encuentra actualmente disponible")
	return render(request, 'publicacion/publicacion.html',{'pub':pub})

def ver_rubro(request,id):
	try:
		publicaciones=Publicacion.objects.filter(rubro=id)
	except Rubro.DoesNotExist:
		raise Http404("Este rubro no se encuentra actualmente disponible")
	return render(request, 'rubro/rubro.html',{'publicaciones':publicaciones})


