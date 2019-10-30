
from django.db import models
from django.contrib.auth.models import User 
# Create your models here.


class Usuario(User):
	TIPO_USUARIOS = (('co','CONSULTAR OFERTAS'),('po','PUBLICAR OFERTAS'))

	tipo_usuario = models.CharField(max_length = 2, null=False, choices = TIPO_USUARIOS) 
	imagen       = models.ImageField(upload_to='fotos_usuarios', null=True,blank=True)

	@property
	def get_locales(self):
		return self.locales.all()

	@property
	def get_locales_id(self):
		locales = self.locales.all()
		list_id_locales = list()
		for local in locales:
			list_id_locales.append(local.id)
			
		return list_id_locales

class Localidad(models.Model):
	nombre = models.CharField(max_length = 30)

	def __str__(self):
		return self.nombre


	def get_locales(self):
	 	return self.locales.all()


class Local(models.Model):
	HORARIOS = ('sh','Abierto según horario'),('24hs','Abierto las 24hs')
	OP_DELIVERY = ((True,'Sí'),(False,'No'))

	nombre     = models.CharField(max_length = 30)
	direccion  = models.CharField(max_length = 50)
	horario    = models.CharField(max_length = 4, choices = HORARIOS)
	usuario    = models.ForeignKey(User, on_delete = models.CASCADE, related_name = 'locales')
	localidad  = models.ForeignKey(Localidad, on_delete = models.CASCADE, related_name = 'locales', null=True)
	delivery   = models.BooleanField(default=False, choices=OP_DELIVERY)
	telefono   = models.IntegerField(null=True,blank=True)
	metodo_pago =  models.ManyToManyField("MedioDePago", through="LocalMedioDePago")
	imagen     = models.ImageField(upload_to='fotos_locales', null=True, blank=True)

	def get_horarios(self):
		return self.horas.all()

	def get_sucursales(self):
		return self.sucursales.all()

	def get_publicaciones(self):
		return self.publicaciones.all()

	def get_medios_de_pago(self):
		return self.medios_de_pago.all()

	def __str__(self):
		return self.nombre


class Sucursal(models.Model):
	direccion = models.CharField(max_length = 50)
	local     = models.ForeignKey(Local, on_delete = models.CASCADE, related_name='sucursales') 
	localidad = models.ForeignKey(Localidad, on_delete = models.CASCADE, related_name='sucursales')
	telefono  = models.IntegerField(null=True,blank=True)


class Horario(models.Model):
	local   = models.ForeignKey(Local, on_delete = models.CASCADE, related_name='horas')
	dia     = models.CharField(max_length = 11)
	hora_d1 = models.CharField(max_length = 5)
	hora_h1 = models.CharField(max_length = 5)
	hora_d2 = models.CharField(max_length = 5, null=True, blank = True)
	hora_h2 = models.CharField(max_length = 5, null=True, blank = True)


class Rubro(models.Model):
	nombre = models.CharField(max_length = 25)
	imagen = models.FileField(upload_to='fotos_rubros', null=True,blank=True)

	def __str__(self):
		return self.nombre

class Publicacion(models.Model):
	local          = models.ForeignKey(Local, on_delete = models.CASCADE, related_name = 'publicaciones')
	rubro   	   = models.ForeignKey(Rubro, on_delete = models.CASCADE, related_name = 'publicaciones')
	titulo         = models.CharField(max_length = 30, null=False)
	detalle        = models.CharField(max_length = 300)
	imagen         = models.ImageField(upload_to='fotos_publicaciones', null=True,blank=True)
	precio_regular = models.DecimalField(max_digits=10, decimal_places=2)
	precio_oferta  = models.DecimalField(max_digits=10, decimal_places=2,null=True,blank=True)
	fecha_creacion = models.DateTimeField(auto_now_add=True, editable=False)
	fecha_publi    = models.DateTimeField(auto_now_add=True)
	activada 	   = models.BooleanField(default=False)
	tiempo_publi   = models.IntegerField(default=1440)
	cant_visitas   = models.IntegerField(default=0)

	def __str__(self):
		return self.titulo

	def get_descuento(self):
		descuento = 100 - int(self.precio_oferta * 100 / self.precio_regular)
		return descuento

	class Meta:
		ordering = ['fecha_publi']



class Favorito(models.Model):
	usuario = models.ForeignKey(Usuario, on_delete = models.CASCADE, related_name = 'favoritos')	
	local   = models.ForeignKey(Local, on_delete = models.CASCADE, related_name = 'favoritos')


class Interes(models.Model):
	usuario = models.ForeignKey(Usuario, on_delete = models.CASCADE, related_name = 'intereses')
	rubro   = models.ForeignKey(Rubro, on_delete = models.CASCADE, related_name = 'intereses')


class MedioDePago(models.Model):
	nombre = models.CharField(max_length = 20, null=False,blank=False)

	class Meta:
		ordering = ['nombre']

	def __str__(self):
		return self.nombre

class LocalMedioDePago(models.Model):
	local = models.ForeignKey(Local, on_delete=models.CASCADE, related_name='medios_de_pago')
	medio_de_pago = models.ForeignKey(MedioDePago, on_delete=models.CASCADE)
	
