from django import forms
from app_ofertas.models import Local, Publicacion, Localidad, MedioDePago, Sucursal

class LocalForm(forms.ModelForm):
	class Meta:
		model = Local
		fields = ('imagen',
			      'nombre',
			      'direccion',
			      'telefono',			      
			      'localidad',
			      'delivery',
			      'metodo_pago',
			      'horario',)

	
class PublicacionForm(forms.ModelForm):
	class Meta:
		model = Publicacion
		fields = ('local',
			'rubro',
			'titulo',
			'detalle',
			'imagen',
			'precio_regular',
			'precio_oferta',
			'activada',
			'tiempo_publi',
			'cant_visitas',
			)


class OfertaForm(forms.ModelForm):
	class Meta:
		model = Publicacion
		fields = ('rubro',
			'titulo',
			'precio_regular',
			'precio_oferta',
			'imagen',
			'detalle',
			)



class SucursalForm(forms.ModelForm):
	class Meta:
		model = Sucursal
		fields= ('localidad',				 
				 'direccion',
				 'telefono')


class EditarLocalForm(forms.ModelForm):
	class Meta:
		model = Local
		fields = ('imagen',
			      'nombre',
			      'direccion',
			      'telefono',			      
			      'localidad',
			      'delivery',
			      'metodo_pago',
			      'horario',)
