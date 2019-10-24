from django.urls import path
from . import views

app_name = 'app_accounts'

urlpatterns = [
    path('login', views.login_view, name='login'),
    path('logout', views.logout_view, name='logout'),
    path('signup', views.create_user_view, name='signup'),
]


