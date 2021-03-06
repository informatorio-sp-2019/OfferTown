from django.shortcuts import render,redirect

from app_ofertas.models import Publicacion,Rubro, Local, MedioDePago, Interes, Favorito, Horario
from app_ofertas.forms import LocalForm, PublicacionForm, OfertaForm, SucursalForm, EditarLocalForm, EditarOfertaForm, HorarioForm
from django.contrib.auth.decorators import login_required
from datetime import date
import ipdb
from django.http import Http404
from django.http import JsonResponse
from django.contrib import messages

# Create your views here.

def hometest(request):
	return render(request, 'esquema.html',{})

#HOME
def index(request):
	#Obtener 30 ofertas recientes activas ordenadas por fecha de creacion
	query=Publicacion.objects.all().filter(activada=True).order_by("fecha_creacion")[:30]
	#de esas 30 mezclar orden y tomar solo 12
	recientes=Publicacion.objects.filter(id__in=query).order_by("?")[:12]
	# categorias para mostrar los rubros 
	categorias = Rubro.objects.all().order_by('nombre')
		
	return render(request,'home.html',{'recientes':recientes, 'categorias':categorias})


#Manda a search_result, con las publicaciones y parametros de la busqueda
def search(request):	
	# parametros
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
			id_pago = MedioDePago.objects.get(nombre="DÉBITO").id
		except:
			pass		
	elif (param_payment =="PAY_CREDIT"):
		try:
			id_pago = MedioDePago.objects.get(nombre="CRÉDITO").id
		except:
			pass
	else:
		pass
	if(id_pago!=0):
		publicaciones = publicaciones.filter(local__metodo_pago = id_pago)
	
	#filtrar delivery
	if (param_delivery=="SI"):
		publicaciones = publicaciones.filter(local__delivery=True)
	else:
		print(param_delivery)
	
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

	#locales que entre dentro de param titulo
	locales = Local.objects.filter(nombre__contains=param_titulo)
	#rubros que entre dentro de param titulo
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
			local = form.save(commit=False)
			local.usuario = request.user.usuario
			local.save()
			if local.horario == 'sh':
				return redirect('app_ofertas:horarios',local=local.nombre, id_local=local.id)
			else:
				return redirect('app_ofertas:ver_local_usuario', usuario = request.user.username, id=local.id)
			
	form = LocalForm()
	context={'form':form}
	template = 'local/alta_local.html'

	return render(request, template, context)


@login_required
def favoritos(request):
	#lugares favoritos
	locales = Local.objects.all().filter(favoritos__usuario=request.user.usuario)
	contexto = {
		"locales":locales
	}
	return render(request, "favoritos.html", contexto)


def tendencia(request):
	#publicaciones activas ordenadas por cantidad de visitas, y tomar las 30 mas visitadas
	query=Publicacion.objects.filter(activada=True).order_by("cant_visitas")[:30]
	#mezclar esas 30 y tomar solo 12
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
	#actualizar visitas
	pub.cant_visitas = pub.cant_visitas +1
	pub.save()

	hoy = dia_spanish()
	horarios = pub.local.get_horarios()
	sucursales = pub.local.get_sucursales()
	medios = pub.local.get_medios_de_pago()
	rubro_pub = pub.rubro
	#relacionados: publicaciones del mismo rubro q pub excepto la pub, orden aleatorio, q esten activas, y tomar solo 4
	relacionados = Publicacion.objects.filter(rubro=rubro_pub).exclude(pk=pub.id).order_by("?").filter(activada=True)[:4]
	return render(request, 'publicacion/publicacion.html',{'pub':pub, "relacionados":relacionados, 'medios':medios, 'sucursales':sucursales, 'horarios':horarios, 'hoy':hoy})

def ver_rubro(request,id):
	try:
		publicaciones=Publicacion.objects.filter(rubro=id).filter(activada=True)
	except Rubro.DoesNotExist:
		raise Http404("Este rubro no se encuentra actualmente disponible")
	
	cantidad = Publicacion.objects.filter(rubro=id).filter(activada=True).count()
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
	mensaje_horario = ''
	if local.horario == '24hs':
		mensaje_horario = 'ABIERTO LAS 24HS.'

	horarios = local.get_horarios()
	ofertas = Publicacion.objects.filter(local=local).filter(activada=True)
	return render(request, 'local/local.html',{'local':local, 'medios':medios, 'horarios':horarios, 'ofertas':ofertas, 'hoy':hoy,'mensaje_horario':mensaje_horario })

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
	medios = local.get_medios_de_pago()
	mensaje_horario = ''
	if local.horario =='24hs':
		mensaje_horario = 'ABIERTO LAS 24HS.'

	horarios = local.get_horarios()
	return render(request, 'local/local_usuario.html',{'local':local, 'ofertas':ofertas, 'medios':medios, 'horarios':horarios, 'mensaje_horario':mensaje_horario})



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
		else:			
			messages.error(request, "Algo salió mal, controle los datos ingresados.")			
		
	else:		
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


def horarios(request,local,id_local):
	# ipdb.set_trace()
	horarios = Local.objects.get(pk=id_local).get_horarios()
	if horarios:
		return redirect('app_ofertas:editar_horarios', local = local, id_local=id_local)	

	if request.method == 'POST':
		local = Local.objects.get(pk=id_local)
		# ipdb.set_trace()
		horamd1 = request.POST['horamd1']
		if horamd1:
			horamh1 = request.POST['horamh1']
			horatd1 = request.POST['horatd1']
			horath1 = request.POST['horath1']
			hora = Horario()
			hora.dia = 'Lunes'
			hora.hora_d1 = horamd1
			hora.hora_h1 = horamh1
			hora.hora_d2 = horatd1
			hora.hora_h2 = horath1
			hora.local = local
			hora.save()

		horamd2 = request.POST['horamd2']
		if horamd2:
			horamh2 = request.POST['horamh2']
			horatd2 = request.POST['horatd2']
			horath2 = request.POST['horath1']
			hora = Horario()
			hora.dia = 'Martes'
			hora.hora_d1 = horamd2
			hora.hora_h1 = horamh2
			hora.hora_d2 = horatd2
			hora.hora_h2 = horath2
			hora.local = local
			hora.save()

		horamd3 = request.POST['horamd3']
		if horamd3:
			horamh3 = request.POST['horamh3']
			horatd3 = request.POST['horatd3']
			horath3 = request.POST['horath3']
			hora = Horario()
			hora.dia = 'Miércoles'
			hora.hora_d1 = horamd3
			hora.hora_h1 = horamh3
			hora.hora_d2 = horatd3
			hora.hora_h2 = horath3
			hora.local = local
			hora.save()

		horamd4 = request.POST['horamd4']
		if horamd4:
			horamh4 = request.POST['horamh4']
			horatd4 = request.POST['horatd4']
			horath4 = request.POST['horath4']
			hora = Horario()
			hora.dia = 'Jueves'
			hora.hora_d1 = horamd4
			hora.hora_h1 = horamh4
			hora.hora_d2 = horatd4
			hora.hora_h2 = horath4
			hora.local = local
			hora.save()

		horamd5 = request.POST['horamd5']
		if horamd5:		
			horamh5 = request.POST['horamh5']
			horatd5 = request.POST['horatd5']
			horath5 = request.POST['horath5']
			hora = Horario()
			hora.dia = 'Viernes'
			hora.hora_d1 = horamd5
			hora.hora_h1 = horamh5
			hora.hora_d2 = horatd5
			hora.hora_h2 = horath5
			hora.local = local
			hora.save()

		horamd6 = request.POST['horamd6']
		if horamd6:		
			horamh6 = request.POST['horamh6']
			horatd6 = request.POST['horatd6']
			horath6 = request.POST['horath6']
			hora = Horario()
			hora.dia = 'Sábado'
			hora.hora_d1 = horamd6
			hora.hora_h1 = horamh6
			hora.hora_d2 = horatd6
			hora.hora_h2 = horath6
			hora.local = local
			hora.save()

		horamd7 = request.POST['horamd7']
		if horamd7:		
			horamh7 = request.POST['horamh7']
			horatd7 = request.POST['horatd7']
			horath7 = request.POST['horath7']
			hora = Horario()
			hora.dia = 'Domingo'
			hora.hora_d1 = horamd7
			hora.hora_h1 = horamh7
			hora.hora_d2 = horatd7
			hora.hora_h2 = horath7
			hora.local = local
			hora.save()

		# ipdb.set_trace()
		return redirect('app_ofertas:ver_local_usuario', usuario = request.user.username, id=id_local)	
		
	form = HorarioForm()			
	template = 'local/alta_horarios2.html'
	context = {'form':form}
	return render(request, template,context)


class Horarios():
	dia1 = ''
	horamd1 = ''
	horamh1 = ''
	horatd1 = ''
	horath1 = ''	
	
	dia2 = ''
	horamd2 = ''
	horamh2 = ''
	horatd2 = ''
	horath2 = ''	
	
	dia3 = ''
	horamd3 = ''
	horamh3 = ''
	horatd3 = ''
	horath3 = ''	
	
	dia4 = ''
	horamd4 = ''
	horamh4 = ''
	horatd4 = ''
	horath4 = ''	

	dia5 = ''
	horamd5 = ''
	horamh5 = ''
	horatd5 = ''
	horath5 = ''	

	dia6 = ''
	horamd6 = ''
	horamh6 = ''
	horatd6 = ''
	horath6 = ''	

	dia7 = ''
	horamd7 = ''
	horamh7 = ''
	horatd7 = ''
	horath7 = ''	



def editar_horarios(request,local,id_local):
	if request.method == 'GET':		
		
		horarios = Local.objects.get(pk=id_local).get_horarios()
		horario = Horarios()
		# ipdb.set_trace()
		for h in horarios:
			if h.dia == 'Lunes':
				horario.dia1 = h.dia
				horario.horamd1 = h.hora_d1
				horario.horamh1 = h.hora_h1
				horario.horatd1 = h.hora_d2
				horario.horath1 = h.hora_h2				
			elif h.dia == 'Martes':
				horario.dia2 = h.dia
				horario.horamd2 = h.hora_d1
				horario.horamh2 = h.hora_h1
				horario.horatd2 = h.hora_d2
				horario.horath2 = h.hora_h2
			elif h.dia == 'Miércoles':
				horario.dia3 = h.dia
				horario.horamd3 = h.hora_d1
				horario.horamh3 = h.hora_h1
				horario.horatd3 = h.hora_d2
				horario.horath3 = h.hora_h2
			elif h.dia == 'Jueves':
				horario.dia4 = h.dia
				horario.horamd4 = h.hora_d1
				horario.horamh4 = h.hora_h1
				horario.horatd4 = h.hora_d2
				horario.horath4 = h.hora_h2
			elif h.dia == 'Viernes':
				horario.dia5 = h.dia
				horario.horamd5 = h.hora_d1
				horario.horamh5 = h.hora_h1
				horario.horatd5 = h.hora_d2
				horario.horath5 = h.hora_h2
			elif h.dia == 'Sábado':
				horario.dia6 = h.dia
				horario.horamd6 = h.hora_d1
				horario.horamh6 = h.hora_h1
				horario.horatd6 = h.hora_d2
				horario.horath6 = h.hora_h2
			elif h.dia == 'Domingo':
				horario.dia7 = h.dia
				horario.horamd7 = h.hora_d1
				horario.horamh7 = h.hora_h1
				horario.horatd7 = h.hora_d2
				horario.horath7 = h.hora_h2

	
		template = 'local/editar_horarios.html'
		context  = {'form':horario} 
		
		return render(request,template,context)
	else:
		Horario.objects.filter(local_id=id_local).delete()

		local = Local.objects.get(pk=id_local)
		# ipdb.set_trace()
		horamd1 = request.POST['horamd1']
		if horamd1:
			horamh1 = request.POST['horamh1']
			horatd1 = request.POST['horatd1']
			horath1 = request.POST['horath1']
			hora = Horario()
			hora.dia = 'Lunes'
			hora.hora_d1 = horamd1
			hora.hora_h1 = horamh1
			hora.hora_d2 = horatd1
			hora.hora_h2 = horath1
			hora.local = local
			hora.save()

		horamd2 = request.POST['horamd2']
		if horamd2:
			horamh2 = request.POST['horamh2']
			horatd2 = request.POST['horatd2']
			horath2 = request.POST['horath2']
			hora = Horario()
			hora.dia = 'Martes'
			hora.hora_d1 = horamd2
			hora.hora_h1 = horamh2
			hora.hora_d2 = horatd2
			hora.hora_h2 = horath2
			hora.local = local
			hora.save()

		horamd3 = request.POST['horamd3']
		if horamd3:
			horamh3 = request.POST['horamh3']
			horatd3 = request.POST['horatd3']
			horath3 = request.POST['horath3']
			hora = Horario()
			hora.dia = 'Miércoles'
			hora.hora_d1 = horamd3
			hora.hora_h1 = horamh3
			hora.hora_d2 = horatd3
			hora.hora_h2 = horath3
			hora.local = local
			hora.save()

		horamd4 = request.POST['horamd4']
		if horamd4:
			horamh4 = request.POST['horamh4']
			horatd4 = request.POST['horatd4']
			horath4 = request.POST['horath4']
			hora = Horario()
			hora.dia = 'Jueves'
			hora.hora_d1 = horamd4
			hora.hora_h1 = horamh4
			hora.hora_d2 = horatd4
			hora.hora_h2 = horath4
			hora.local = local
			hora.save()

		horamd5 = request.POST['horamd5']
		if horamd5:		
			horamh5 = request.POST['horamh5']
			horatd5 = request.POST['horatd5']
			horath5 = request.POST['horath5']
			hora = Horario()
			hora.dia = 'Viernes'
			hora.hora_d1 = horamd5
			hora.hora_h1 = horamh5
			hora.hora_d2 = horatd5
			hora.hora_h2 = horath5
			hora.local = local
			hora.save()

		horamd6 = request.POST['horamd6']
		if horamd6:		
			horamh6 = request.POST['horamh6']
			horatd6 = request.POST['horatd6']
			horath6 = request.POST['horath6']
			hora = Horario()
			hora.dia = 'Sábado'
			hora.hora_d1 = horamd6
			hora.hora_h1 = horamh6
			hora.hora_d2 = horatd6
			hora.hora_h2 = horath6
			hora.local = local
			hora.save()

		horamd7 = request.POST['horamd7']
		if horamd7:		
			horamh7 = request.POST['horamh7']
			horatd7 = request.POST['horatd7']
			horath7 = request.POST['horath7']
			hora = Horario()
			hora.dia = 'Domingo'
			hora.hora_d1 = horamd7
			hora.hora_h1 = horamh7
			hora.hora_d2 = horatd7
			hora.hora_h2 = horath7
			hora.local = local
			hora.save()

		return redirect('app_ofertas:ver_local_usuario', usuario = request.user.username, id=id_local)	

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

	if (oferta.local.usuario.id == request.user.usuario.id):
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
	rubros = Rubro.objects.all()
	template='intereses/seteo_intereses.html'  
	context = {'rubros':rubros}
	return render(request,template,context)	

	
@login_required
def editar_local(request,usuario,id):
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

def creditos(request):
	return render(request, 'creditos.html',{})