from django.urls import path,include
from . import views


urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('profile', views.ProfileView.as_view(), name='profile'),
    path('login', views.LoginView.as_view(), name='login')
]