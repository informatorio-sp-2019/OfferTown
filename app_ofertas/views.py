from django.shortcuts import render,redirect

from app_ofertas.models import Publicacion,Rubro, Local, MedioDePago, Interes, Favorito
from app_ofertas.forms import LocalForm, PublicacionForm, OfertaForm, SucursalForm, EditarLocalForm, EditarOfertaForm
from django.contrib.auth.decorators import login_required
from datetime import date
import ipdb
from django.http import Http404
from django.http import JsonResponse

# Create your views here.

def hometest(request):
	return render(request, 'esquema.html',{})

def index(request):
	#Obtener 9 ofertas recientes (mando todas mientras CORREGIR )
	query=Publicacion.objects.all().filter(activada=True).order_by("fecha_creacion")[:30]
	recientes=Publicacion.objects.filter(id__in=query).order_by("?")[:12]
	
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
	publicaciones = Publicacion.objects.filter(titulo__contains=param_titulo).filter(activada=True)

	#filtrar metodo pago
	id_pago = 0

	if (param_payment=="PAY_CASH"):
		try:
			id_pago = MedioDePago.objects.get(nombre="EFECTIVO").id
		except:
			pass
	elif (param_payment=="PAY_DEBIT"):
		try:
			id_pago = MedioDePago.objects.get(nombre="DEBITO").id
		except:
			pass		
	elif (param_payment =="PAY_CREDIT"):
		try:
			id_pago = MedioDePago.objects.get(nombre="CREDITO").id
		except:
			pass
	else:
		pass

	if(id_pago!=0):
		publicaciones = publicaciones.filter(local__metodo_pago = id_pago)
	
	#filtrar delivery
	if (param_delivery=="SI"):
		publicaciones = publicaciones.filter(local__delivery=True)
	elif (param_delivery=="NO"):
		publicaciones = publicaciones.filter(local__delivery=False)
	else:
		print(param_delivery)

	#agregar las publicaciones  rubros que entre dentro de param titulo
	#

	#ordenar
	if (param_orden == "1"):
		#de menor a mayor precio
		publicaciones = publicaciones.order_by('precio_oferta','precio_regular')
	elif (param_orden == "2"):
		#de mayor a menor precio
		publicaciones = publicaciones.order_by('-precio_oferta','-precio_regular')
	else:
		#por abecedario
		publicaciones = publicaciones.order_by('titulo')


	locales = Local.objects.filter(nombre__contains=param_titulo)
	rubros = Rubro.objects.filter(nombre__contains=param_titulo)

	#preparar contexto para el template
	contexto = {
		"publicaciones":publicaciones,
		"locales":locales,
		"rubros":rubros,
		"param_titulo": param_titulo,
		"param_payment": param_payment,
		"param_delivery": param_delivery,
		"param_orden": param_orden
	}

	return render(request, "search/search_results.html", contexto)
#fin Search()

@login_required
def agregar_local(request):
	
	if request.method == 'POST':
		form = LocalForm(request.POST, request.FILES)
		if form.is_valid():
			# ipdb.set_trace()
			local = form.save(commit=False)
			local.usuario = request.user.usuario
			local.save()
			
			return redirect('app_ofertas:ver_local_usuario', usuario = request.user.username, id=local.id)
			
	form = LocalForm()
	context={'form':form}
	template = 'local/alta_local.html'

	return render(request, template, context)

# def agregar_publicacion(request):
# 	if request.method == 'POST':
# 		form = PublicacionForm(request.POST)
# 		if form.is_valid():
# 			form.save()

# 			return redirect('app_ofertas:ver_local_usuario', usuario = request.user.username, id=id)

# 	form = PublicacionForm()
# 	return render(request, 'publicacion/agregar_publicacion.html',{'form':form})


@login_required
def favoritos(request):
	#lugares favoritos
	locales = Local.objects.all().filter(favoritos__usuario=request.user.usuario)
	contexto = {
		"locales":locales
	}
	return render(request, "favoritos.html", contexto)


def tendencia(request):
	query=Publicacion.objects.filter(activada=True).order_by("cant_visitas")[:30]
	tendencias=Publicacion.objects.filter(id__in=query).order_by("?")[:12]	

	
	contexto = {
		"tendencias":tendencias
	}
	return render(request, "tendencia.html", contexto)

@login_required
def intereses(request):
	#publicaciones rubros favoritos
	rubros = Rubro.objects.all().filter(intereses__usuario=request.user.usuario)  
	contexto = {
		"rubros":rubros
	}
	return render(request, "intereses.html", contexto)

def ver_publicacion(request,id):
	try:
		pub=Publicacion.objects.get(pk=id)
	except Publicacion.DoesNotExist:
		raise Http404("Esta oferta no se encuentra actualmente disponible")

	if not pub.activada:
		raise Http404("Esta oferta no se encuentra actualmente disponible")

	pub.cant_visitas = pub.cant_visitas +1
	pub.save()
	hoy = dia_spanish()
	horarios = pub.local.get_horarios()
	sucursales = pub.local.get_sucursales()
	medios = pub.local.get_medios_de_pago()
	rubro_pub = pub.rubro
	relacionados = Publicacion.objects.filter(rubro=rubro_pub).exclude(pk=pub.id).order_by("?").filter(activada=True)[:4]
	return render(request, 'publicacion/publicacion.html',{'pub':pub, "relacionados":relacionados, 'medios':medios, 'sucursales':sucursales, 'horarios':horarios, 'hoy':hoy})

def ver_rubro(request,id):
	try:
		publicaciones=Publicacion.objects.filter(rubro=id)
	except Rubro.DoesNotExist:
		raise Http404("Este rubro no se encuentra actualmente disponible")
	
	cantidad = Publicacion.objects.filter(rubro=id).count()
	rubro= Rubro.objects.get(pk=id)
	return render(request, 'rubro/rubro.html',{'publicaciones':publicaciones, 'rubro':rubro, 'cantidad':cantidad})

def dia_spanish():
	hoy = date.today().strftime("%A")

	if hoy == "Monday":
		hoy = "Lunes"
	elif hoy == "Tuesday":
		hoy = "Martes"
	elif hoy== "Wednesday":
		hoy = "Miércoles"
	elif hoy == "Thursday":
		hoy = "Jueves"
	elif hoy == "Friday":
		hoy = "Viernes"
	elif hoy == "Saturday":
		hoy = "Sábado"
	else:
		hoy = "Domingo"

	return hoy


def ver_local(request,id):
	try:		
		local=Local.objects.get(pk=id)
	except Local.DoesNotExist:
		raise Http404("Este local no se encuentra actualmente disponible")

	hoy = dia_spanish()
	medios = local.get_medios_de_pago()
	horarios = local.get_horarios()
	ofertas = Publicacion.objects.filter(local=local)
	return render(request, 'local/local.html',{'local':local, 'medios':medios, 'horarios':horarios, 'ofertas':ofertas, 'hoy':hoy })

@login_required
def ver_local_usuario(request,usuario,id):
	if request.user.username == usuario and (id in request.user.usuario.get_locales_id):
		try:
			local=Local.objects.get(pk=id)
		except Local.DoesNotExist:
			raise Http404("Este local no se encuentra actualmente disponible")
	else:
		raise Http404("Este local no se encuentra actualmente disponible")

	ofertas = Publicacion.objects.filter(local=local)
	return render(request, 'local/local_usuario.html',{'local':local, 'ofertas':ofertas})


#	hoy = dia_spanish()
#	medios = local.get_medios_de_pago()
#	horarios = local.get_horarios()
#	ofertas = Publicacion.objects.filter(local=local)
#	return render(request, 'local/local_usuario.html',{'local':local, 'medios':medios, 'horarios':horarios, 'ofertas':ofertas, 'hoy':hoy })


def vistas_test(request):
	#Obtener 9 ofertas recientes (mando todas mientras CORREGIR )
	recientes=Publicacion.objects.all()
	#últimas 9
	#recientes=Publicacion.objects.order_by('-id')[:9]
	#Obtener las categorías
	categorias = Rubro.objects.all().order_by('nombre')

	return render(request,'vistas_test.html',{'publicaciones':recientes, 'rubros':categorias})


def ver_perfil_usuario(request):
	# usuario = usuario
	usuario = request.user.usuario
	return render(request, 'perfil/perfil.html', {'usuario':usuario})

@login_required
def nueva_oferta(request,usuario,id):
	if request.method == 'POST':
		form = OfertaForm(request.POST, request.FILES)
		if form.is_valid():
			local = Local.objects.get(pk=id)
			oferta = form.save(commit=False)
			oferta.local = local
			oferta.save()
			
			return redirect('app_ofertas:ver_local_usuario', usuario = request.user.username, id=id)
			
	form = OfertaForm()
	context={'form':form}
	template = 'publicacion/nueva_oferta.html'

	return render(request, template, context)

@login_required
def editar_ofertas(request,usuario,id):
	if request.user.username == usuario and (id in request.user.usuario.get_locales_id):
		try:
			local=Local.objects.get(pk=id)
		except Local.DoesNotExist:
			raise Http404("Este local no se encuentra actualmente disponible")
	else:
		raise Http404("Este local no se encuentra actualmente disponible")

	ofertas = Publicacion.objects.filter(local=local)
	cantidad = Publicacion.objects.filter(local=local).count()

	return render(request, 'publicacion/editar_publicaciones.html', {'usuario':usuario, 'local':local, 'ofertas':ofertas, 'cantidad':cantidad})





def horarios(request):
	return render(request, 'local/alta_horarios.html',{})


#@login_required
#def mis_ofertas(request,usuario):
#	try:
#		locales = Local.objects.filter(usuario=usuario)

#	MATIAS ACÁ NO SE COMO AGREGAR AL QUERYSET LAS OFERTAS DE LOS DISITNTOS LOCALES YA QUE FILTRO LAS OFERTAS DE A UN LOCAL EN LA CONSULTA


#		for local in locales:
#			ofertas = Publicacion.objects.filter(local = local)
#
#		ofertas=Publicacion.objects.filter(local__usuario=request.user.username)
#	except Rubro.DoesNotExist:
#		raise Http404("no hay publicaciones")
#	
#	return render(request, 'publicacion/mis_ofertas.html',{'publicaciones':ofertas})

@login_required
def nueva_sucursal(request,usuario,id):
	
	if request.method == 'POST':
		form = SucursalForm(request.POST)
		if form.is_valid():
			sucursal = form.save(commit=False)
			sucursal.local = Local.objects.get(pk=id)
			sucursal.save()
			
			return redirect('app_ofertas:ver_local_usuario', usuario = request.user.username, id=id)	
			
	form = SucursalForm()
	context={'form':form}
	template = 'local/alta_sucursal.html'

	return render(request, template, context)


# @login_required
# def nueva_oferta(request,usuario,id):
# 	if request.method == 'POST':
# 		form = OfertaForm(request.POST, request.FILES)
# 		if form.is_valid():
# 			local = Local.objects.get(pk=id)
# 			oferta = form.save(commit=False)
# 			oferta.local = local
# 			oferta.save()
			
# 			return redirect('app_ofertas:index')	
			
# 	form = OfertaForm()
# 	context={'form':form}
# 	template = 'publicacion/nueva_oferta.html'

# 	return render(request, template, context)







def toggleInteres(request, id):
	rubro = Rubro.objects.get(pk=id)

	new_interes, created = Interes.objects.get_or_create(usuario=request.user.usuario, rubro=rubro)
  

	if created:
		estado="SI"
	else:
		new_interes.delete()
		estado="NO"

	data = {}
	

	data = {
		"id":rubro.id,
		"estado":estado
	}

	return JsonResponse(data)


def toggleFavorito(request, id):
	local = Local.objects.get(pk=id)

	new_favorito, created = Favorito.objects.get_or_create(usuario=request.user.usuario, local=local)
  

	if created:
		estado="SI"
	else:
		new_favorito.delete()
		estado="NO"

	data = {}
	

	data = {
		"id":local.id,
		"estado":estado
	}

	return JsonResponse(data)
def toggleActivadoOferta(request,id):
	oferta = Publicacion.objects.get(pk=id)
	data = {}
	estado = ""
	print("a")
	print(estado)
	print(oferta.local.usuario)
	print(request.user.usuario)

	if (oferta.local.usuario.id == request.user.usuario.id):
		print("usuario igual")
		if oferta.activada:
			oferta.activada = False
			oferta.save()
			estado="NO"
		else:
			oferta.activada = True
			oferta.save()
			estado="SI"

		data = {
			"id":oferta.id,
			"estado":estado
		}
	else:
		print("usuario distinto")


	return JsonResponse(data)

class SetIntereses():
	def __init__(self,nombre,id,valor):
		self.nombre =nombre
		self.id     = id
		self.valor  = valor

	def __str__(self):
		return 'Rubro: {}, Id: {}, Valor: {}'.format(self.nombre,self.id,self.valor)


def set_intereses(request):

	#ipdb.set_trace()

	rubros = Rubro.objects.all()
	template='intereses/seteo_intereses.html'  
	context = {'rubros':rubros}
	return render(request,template,context)	

	
@login_required
def editar_local(request,usuario,id):
	# ipdb.set_trace()
	local = Local.objects.get(pk=id)
	if request.method == 'GET':
		form = EditarLocalForm(instance = local)
	else:
		form = EditarLocalForm(request.POST, request.FILES, instance = local)
		if form.is_valid():
			local = form.save(commit=False)
			local.usuario = request.user.usuario
			local.save()

			return redirect('app_ofertas:ver_local_usuario', usuario = request.user.username, id=id)	

	contexto = {'form':form}
	template = 'local/editar_local.html'
	return render(request,template,contexto)

def comprobar_usuario(request,usuario):
	if request.user.username == usuario:
		return True
	else:
		return False

@login_required
def eliminar_oferta(request,usuario,id,id_oferta):
	if comprobar_usuario(request,usuario):
		Publicacion.objects.filter(id=id_oferta).delete()	
	else:
		raise Http404("No se encuentra habilitado para realizar ésta operación!")		

	return redirect('app_ofertas:editar_ofertas', usuario = request.user.username, id=id)	
	

@login_required
def re_editar_oferta(request,usuario,id,id_oferta):
	if not comprobar_usuario(request,usuario):
		raise Http404("No se encuentra habilitado para realizar ésta operación!")		
	else:
		q_oferta = Publicacion.objects.get(pk=id_oferta)
		if request.method == 'GET':
			form = EditarOfertaForm(instance = q_oferta)
		else:
			form = EditarOfertaForm(request.POST, request.FILES, instance = q_oferta)
			if form.is_valid():
				oferta = form.save(commit=False)
				oferta.usuario = request.user.usuario
				oferta.save()
					
				return redirect('app_ofertas:editar_ofertas', usuario = request.user.username, id=id)	

	template = 'publicacion/re_editar_oferta.html'
	context  = {'form':form}
	return render(request,template,context)
