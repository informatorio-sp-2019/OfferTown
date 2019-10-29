from django import forms
from app_ofertas.models import Local, Publicacion, Localidad, MedioDePago

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



