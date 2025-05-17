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
    
    # Récupérer date actuelle
    today = date.today()
    
    # Calculer la date de fin (7 jours après)
    end_date = today + timedelta(days=7)
    
    # Récupérer les réservations pour cette salle sur la période
    reservations = Reservation.objects.filter(
        salle=salle,
        date_res__gte=today,
        date_res__lte=end_date
    ).order_by('date_res', 'heure_deb')
    
    # Créer une structure de données pour le calendrier
    calendar_data = []
    
    # Pour chaque jour dans la période
    current_date = today
    while current_date <= end_date:
        # Filtrer les réservations pour ce jour
        day_reservations = reservations.filter(date_res=current_date)
        
        # Ajouter les données à notre calendrier
        calendar_data.append({
            'date': current_date,
            'weekday': current_date.strftime('%A'),
            'reservations': day_reservations,
        })
        
        current_date += timedelta(days=1)
    
    context = {
        'salle': salle,
        'calendar_data': calendar_data,
        'today': today,
        'end_date': end_date,
    }
    
    return render(request, 'Salle/detail_salle.html', context)