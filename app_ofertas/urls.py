from django.urls import path
from app_ofertas import views

app_name = 'app_ofertas'

urlpatterns = [
    path('home/',views.hometest, name='home'),
    path('', views.index, name = 'index'),
    path('search', views.search),
    path('agregar_local/', views.agregar_local, name="agregar_local"),
    path('agregar_publicacion/', views.agregar_publicacion, name='agregar_publicacion'),

    path('favoritos', views.favoritos),
    path('tendencias', views.tendencia),
    path('intereses', views.intereses),

    path('pub/<int:id>/',views.ver_publicacion,name='ver_publicacion'),
    path('loc/<int:id>/', views.ver_local,name='ver_local'),

    path('rubro/<int:id>/',views.ver_rubro,name='ver_rubro'),

    path('vistas_test', views.vistas_test),
    path('<usuario>/<int:id>/', views.ver_local_usuario,name='ver_local_usuario'),
    path('<usuario>/<int:id>/nueva_oferta/', views.nueva_oferta,name='nueva_oferta'),
    path('<usuario>/<int:id>/nueva_sucursal/', views.nueva_sucursal,name='nueva_sucursal'),
#    path('<usuario>/mis_ofertas/', views.mis_ofertas,name='ver_ofertas_usuario'),


    path('<usuario>/perfil/', views.ver_perfil_usuario, name='ver_perfil_usuario')
]
