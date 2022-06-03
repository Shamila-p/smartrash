from django.urls import path
from . import views

urlpatterns = [
    path('home', views.home, name='home'),
    path('set-waste-amount', views.set_waste_amount, name='set_waste_amount'),
]
