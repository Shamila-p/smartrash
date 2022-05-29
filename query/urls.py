from django.urls import path
from . import views

urlpatterns = [
       path('query/ask',views.ask_query,name="ask_query"),
       path('query/display',views.display_query,name="display_query"),

]
