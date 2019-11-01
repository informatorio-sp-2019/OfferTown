from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import LoginForm,CreateForm
from django.contrib import messages
import ipdb

# Create your views here.

def login_view(request):	
	if request.user.is_authenticated:
		return redirect('app_ofertas:index') 

	if request.method == 'POST':
		username_post = request.POST['username']
		password_post = request.POST['password']
		user = authenticate(request,username = username_post,password = password_post)

		if user is not None:
			login(request,user)
			return redirect('app_ofertas:index')
		else:
			messages.error(request, 'Usuario o password incorrecto!!')


	form = LoginForm()
	context = {'form':form}
	template = 'login.html'

	return render(request,template,context)


@login_required
def logout_view(request):
	logout(request)	
	return redirect('app_accounts:login')


def create_user_view(request):
	if request.user.is_authenticated:
		return redirect('app_ofertas:index') 

	if request.method == 'POST':
		form = CreateForm(request.POST, request.FILES)		
		if form.is_valid():
			# ipdb.set_trace()	
			user = form.save(commit=False)
			user.set_password(user.password)
			user.is_staff = True			
			user.save()
			return redirect('app_accounts:login')					

	form = CreateForm()
	context = {'form':form}
	template = 'register.html'

	return render(request,template,context)
