from django.shortcuts import render,redirect
from .forms import LoginForm
from django.contrib.auth import authenticate, login as login_django, logout as logout_django
from django.contrib.auth.decorators import login_required
from django.contrib import messages

def login(request):
	if request.user.is_authenticated:
		return redirect('/')		

	if request.method == "POST":
		username_login = request.POST['username']
		password_login = request.POST['password']
 
		user = authenticate(username=username_login,password=password_login)
		if user is not None:
			login_django(request,user)
			request.session['member_id'] = user.id
			request.session.set_expiry(43200) #86400 = 24hs		
			return redirect('/')
		else:
			messages.error(request, 'Usuario o password incorrecto!!')

	form = LoginForm()
	contexto={'form':form}
	return render(request,'login.html',contexto)

@login_required(login_url='login')
def logout(request):
	logout_django(request)
	return redirect('login')