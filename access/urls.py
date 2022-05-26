from django.urls import path
from .import views

urlpatterns = [
    path('', views.index, name='index'),

    path('customer', views.customer, name='customer'),
    path('customer/login', views.customer_login, name='customer_login'),

    path('agent', views.agent, name='agent'),
    path('agent/login', views.agent_login, name='agent_login'),

    path('municipality', views.municipality, name='municipality'),
    path('municipality/login', views.municipality_login, name='municipality_login'),

    path('admin/', views.admin, name='admin'),
    path('admin/login', views.admin_login, name='admin_login'),

    path('customer/signup', views.customer_signup, name='customer_signup'),
    path('agent/signup', views.agent_signup, name='agent_signup'),

    path('logout', views.logout, name='logout'),
]
