from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Salle
from Reservations.models import Reservation
from datetime import datetime, date, timedelta

@login_required
def Consultation_Salles(request):
    salles = Salle.objects.all()
    return render(request, 'Salle/Accueil.html', {'salles': salles})

@login_required
def detail_salle(request, slug):
    salle = Salle.objects.get(slug=slug)
    return render(request, 'Salle/detail_salle.html', {'salle': salle})
