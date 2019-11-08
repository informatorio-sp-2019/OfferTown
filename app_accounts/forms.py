from django import forms
from app_ofertas.models import Usuario

class LoginForm(forms.Form):
	username = forms.CharField(max_length=30)
	password = forms.CharField(max_length=30,widget=forms.PasswordInput())
	

class CreateForm(forms.ModelForm):
	class Meta:
		model= Usuario
		fields=('imagen',
				'username',
				'first_name',
				'last_name',
				'password',
				'email',
				'tipo_usuario',
				)
		labels = {"tipo_usuario":"Preferencia de uso", }
		widgets = {'password':forms.PasswordInput()}


class UpdatePerfilForm(forms.ModelForm):
	class Meta:
		model= Usuario
		fields=('imagen',
				'username',
				'first_name',
				'last_name',
				'email',
				'tipo_usuario',
				)
		labels = {"tipo_usuario":"Preferencia de uso", }
		widgets = {'password':forms.PasswordInput()}

