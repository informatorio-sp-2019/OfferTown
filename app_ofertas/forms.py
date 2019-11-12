from django import forms
from app_ofertas.models import Local, Publicacion, Localidad, MedioDePago, Sucursal, Horario
import ipdb

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

	def clean(self):

		form_data = self.cleaned_data
		if form_data['precio_regular'] <= form_data['precio_oferta']:
			self._errors['precio_oferta'] = 'El precio de oferta debe ser menor al precio regular.'

		return form_data

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

class EditarOfertaForm(forms.ModelForm):
	class Meta:
		model = Publicacion
		fields = ('rubro',
			'titulo',
			'imagen',
			'detalle',
			)

class HorarioForm(forms.Form):
	dia1 = forms.CharField(max_length=7)
	horamd1 = forms.CharField(max_length=5,required = False,widget=forms.TextInput(attrs={'placeholder': '00:00'}))
	horamh1 = forms.CharField(max_length=5,required = False,widget=forms.TextInput(attrs={'placeholder': '00:00'}))
	horatd1 = forms.CharField(max_length=5,required = False,widget=forms.TextInput(attrs={'placeholder': '00:00'}))
	horath1 = forms.CharField(max_length=5,required = False,widget=forms.TextInput(attrs={'placeholder': '00:00'}))	
	
	dia2 = forms.CharField(max_length=7)
	horamd2 = forms.CharField(max_length=5,required = False,widget=forms.TextInput(attrs={'placeholder': '00:00'}))
	horamh2 = forms.CharField(max_length=5,required = False,widget=forms.TextInput(attrs={'placeholder': '00:00'}))
	horatd2 = forms.CharField(max_length=5,required = False,widget=forms.TextInput(attrs={'placeholder': '00:00'}))
	horath2 = forms.CharField(max_length=5,required = False,widget=forms.TextInput(attrs={'placeholder': '00:00'}))	
	
	dia3 = forms.CharField(max_length=7)
	horamd3 = forms.CharField(max_length=5,required = False,widget=forms.TextInput(attrs={'placeholder': '00:00'}))
	horamh3 = forms.CharField(max_length=5,required = False,widget=forms.TextInput(attrs={'placeholder': '00:00'}))
	horatd3 = forms.CharField(max_length=5,required = False,widget=forms.TextInput(attrs={'placeholder': '00:00'}))
	horath3 = forms.CharField(max_length=5,required = False,widget=forms.TextInput(attrs={'placeholder': '00:00'}))	
	
	dia4 = forms.CharField(max_length=7)
	horamd4 = forms.CharField(max_length=5,required = False,widget=forms.TextInput(attrs={'placeholder': '00:00'}))
	horamh4 = forms.CharField(max_length=5,required = False,widget=forms.TextInput(attrs={'placeholder': '00:00'}))
	horatd4 = forms.CharField(max_length=5,required = False,widget=forms.TextInput(attrs={'placeholder': '00:00'}))
	horath4 = forms.CharField(max_length=5,required = False,widget=forms.TextInput(attrs={'placeholder': '00:00'}))	

	dia5 = forms.CharField(max_length=7)
	horamd5 = forms.CharField(max_length=5,required = False,widget=forms.TextInput(attrs={'placeholder': '00:00'}))
	horamh5 = forms.CharField(max_length=5,required = False,widget=forms.TextInput(attrs={'placeholder': '00:00'}))
	horatd5 = forms.CharField(max_length=5,required = False,widget=forms.TextInput(attrs={'placeholder': '00:00'}))
	horath5 = forms.CharField(max_length=5,required = False,widget=forms.TextInput(attrs={'placeholder': '00:00'}))	

	dia6 = forms.CharField(max_length=7)
	horamd6 = forms.CharField(max_length=5,required = False,widget=forms.TextInput(attrs={'placeholder': '00:00'}))
	horamh6 = forms.CharField(max_length=5,required = False,widget=forms.TextInput(attrs={'placeholder': '00:00'}))
	horatd6 = forms.CharField(max_length=5,required = False,widget=forms.TextInput(attrs={'placeholder': '00:00'}))
	horath6 = forms.CharField(max_length=5,required = False,widget=forms.TextInput(attrs={'placeholder': '00:00'}))	

	dia7 = forms.CharField(max_length=7)
	horamd7 = forms.CharField(max_length=5,required = False,widget=forms.TextInput(attrs={'placeholder': '00:00'}))
	horamh7 = forms.CharField(max_length=5,required = False,widget=forms.TextInput(attrs={'placeholder': '00:00'}))
	horatd7 = forms.CharField(max_length=5,required = False,widget=forms.TextInput(attrs={'placeholder': '00:00'}))
	horath7 = forms.CharField(max_length=5,required = False,widget=forms.TextInput(attrs={'placeholder': '00:00'}))