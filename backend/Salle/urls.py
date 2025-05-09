from django.urls import path
from .views import Consultation_Salles

urlpatterns = [
    path('' , Consultation_Salles , name='Consultation_salles' ), 
]