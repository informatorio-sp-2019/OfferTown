from django.urls import path
from app_ofertas import views

app_name = 'app_ofertas'

urlpatterns = [
    path('home/',views.hometest),
    path('', views.index, name = 'index'),
    path('search', views.search),
    path('agregar_local/', views.agregar_local, name="agregar_local"),
    path('agregar_publicacion/', views.agregar_publicacion, name='agregar_publicacion'),
    path('favoritos', views.favoritos),
    path('tendencia', views.tendencia),
    path('intereses', views.intereses),
]
