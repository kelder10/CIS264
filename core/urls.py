from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('trails/', views.trails, name='trails'),
    path('contact/', views.contact, name='contact'),
    path('api/weather/', views.weather_api, name='weather_api'),
]
