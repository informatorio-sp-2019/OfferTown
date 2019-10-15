from django.urls import path
from app_ofertas import views

app_name = 'app_ofertas'

urlpatterns = [
    path('home/',views.hometest),
]
