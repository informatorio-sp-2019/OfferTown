from django.shortcuts import render

# Create your views here.
def hometest(request):
	return render(request, 'esquema.html',{})
