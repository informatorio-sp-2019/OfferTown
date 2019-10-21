from django import forms
from app_ofertas.models import Local, Publicacion

class LocalForm(forms.ModelForm):
	class Meta:
		model = Local
		fields = ('nombre','direccion','horario','usuario','localidad')

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
			#'fecha_creacion',
			#'fecha_publi'
			)