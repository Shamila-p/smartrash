from django.urls import path
from . import views

urlpatterns = [
    path('booking/create', views.booking_create, name='booking_create'),
    path('list/booking', views.list_booking, name='list_booking'),
    path('booking/detailed_view/<int:booking_id>', views.detailed_view, name='detailed_view'),
    path('history', views.booking_history, name='booking_history'),

    path('collect', views.collect, name='collect'),

    


]