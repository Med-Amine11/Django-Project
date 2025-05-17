from django.urls import path
from .views import Consultation_Salles, detail_salle

urlpatterns = [
    path('', Consultation_Salles, name='Consultation_salles'),
    path('<slug:slug>/', detail_salle, name='detail_salle'),
]