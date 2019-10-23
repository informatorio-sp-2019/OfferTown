from django import forms
from app_ofertas.models import Usuario

class LoginForm(forms.Form):
	username = forms.CharField(max_length=30)
	password = forms.CharField(max_length=30,widget=forms.PasswordInput())
	