from django.urls import path 
from .views import Login , deconnexion


urlpatterns = [
    path('' , Login , name ='login'),
     path('logout/', deconnexion, name='logout'),
]
