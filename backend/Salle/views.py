from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Salle 

# Create your views here.
@login_required
def Consultation_Salles(request) : 
    Salles = Salle.objects.all()
    return render(request,'Salle/Accueil.html',{'Salles' : Salles})