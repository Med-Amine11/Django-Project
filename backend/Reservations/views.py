import json
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from datetime import date, timedelta, datetime
from .forms import ReservationForm
from .models import Reservation
from Salle.models import Salle
from django.utils.safestring import mark_safe
@login_required
def effectuer_reservation(request, salle_id):
    # Vérifier si l'utilisateur a déjà 3 réservations actives
    if Reservation.utilisateur_a_trop_de_reservations(request.user.id):
        messages.error(
            request,
            "Vous avez déjà 3 réservations actives. Vous ne pouvez pas avoir plus de 3 réservations à la fois."
        )
        return redirect('mes_reservations')

    salle = get_object_or_404(Salle, id=salle_id)
    calendar_data = []

    # Préparer le calendrier de disponibilité pour la semaine
    today = date.today()

    if today.weekday() == 5:
        today += timedelta(days=2)
    elif today.weekday() == 6:
        today += timedelta(days=1)

    end_date = today + timedelta(days=7)
    current_date = today

    # Récupérer toutes les réservations pour cette salle sur la période
    reservations = Reservation.objects.filter(
        salle=salle,
        date_res__gte=today,
        date_res__lte=end_date,
        etat='accepte'  # Seulement les réservations acceptées
    ).order_by('date_res', 'heure_deb')

    while current_date < end_date:
        if current_date.weekday() < 5:
            # Filtrer les réservations pour ce jour
            day_reservations = reservations.filter(date_res=current_date)
            # Convertir chaque réservation en dict sérialisable
            serialized_reservations = []
            for res in day_reservations:
                serialized_reservations.append({
                    'debut': res.heure_deb.strftime('%H:%M'),
                    'fin': res.heure_fin.strftime('%H:%M'),
                })
            calendar_data.append({
                'date': current_date.strftime('%Y-%m-%d'),
                'reservations': serialized_reservations,
            })
        current_date += timedelta(days=1)

    if request.method == 'POST':
        form = ReservationForm(request.POST)
        if form.is_valid():
            reservation = form.save(commit=False)
            # Vérifier la disponibilité
            if Reservation.est_disponible(
                salle_id=reservation.salle.id,
                date_res=reservation.date_res,
                heure_deb=reservation.heure_deb,
                heure_fin=reservation.heure_fin
            ):
                reservation.utilisateur = request.user  # <-- correction ici
                reservation.save()
                messages.success(
                    request,
                    "Votre réservation a été effectuée avec succès et est en attente de validation."
                )
                return redirect('mes_reservations')
            else:
                messages.error(
                    request,
                    "La salle n'est pas disponible aux horaires sélectionnés."
                )
    else:
        # Pour un nouveau formulaire, on préremplit la salle si elle est fournie
        initial = {'salle': salle_id} if salle_id else {}
        form = ReservationForm(initial=initial)

    context = {
        'form': form,
        'salle': salle,
        'calendar_data_json': mark_safe(json.dumps(calendar_data))
    }

    return render(request, 'Reservations/reserver.html', context)

@login_required
def mes_reservations(request):
    # Récupérer toutes les réservations de l'utilisateur
    reservations = Reservation.objects.filter(
        utilisateur=request.user
    ).order_by('-date_res', '-heure_deb')
    
    # Pour chaque réservation, vérifier si elle peut être annulée ou modifiée
    for reservation in reservations:
        # Utiliser des noms d'attributs différents pour éviter le conflit avec les méthodes
        reservation.peut_etre_annulee = reservation.peut_annuler()
        reservation.peut_etre_modifiee = reservation.peut_modifier()
    
    # Compter les réservations actives
    reservations_actives = Reservation.objects.filter(
        utilisateur=request.user,
        etat__in=['attente', 'accepte']
    ).count()
    
    context = {
        'reservations': reservations,
        'reservations_actives': reservations_actives,
        'reservations_restantes': 3 - reservations_actives
    }
    
    return render(request, 'Reservations/mes_reservations.html', context)

@login_required
def annuler_reservation(request, reservation_id):
    # Récupérer la réservation ou retourner une erreur 404
    reservation = get_object_or_404(Reservation, id=reservation_id, utilisateur=request.user)
    
    # Vérifier si la réservation peut être annulée
    if not reservation.peut_annuler():
        messages.error(request, "Cette réservation ne peut pas être annulée. L'annulation est possible uniquement jusqu'à 24h avant l'heure de réservation.")
        return redirect('mes_reservations')
    
    if request.method == 'POST':
        # Suppression de la réservation
        reservation.delete()
        messages.success(request, "Votre réservation a été annulée avec succès.")
        return redirect('mes_reservations')
    
    context = {
        'reservations': reservation
    }
    
    return render(request, 'Reservations/annuler_reservation.html', context)

@login_required
def modifier_reservation(request, reservation_id):
    # Récupérer la réservation ou retourner une erreur 404
    reservation = get_object_or_404(Reservation, id=reservation_id, utilisateur=request.user)
    
    # Vérifier si la réservation peut être modifiée
    if not reservation.peut_modifier():
        messages.error(request, "Cette réservation ne peut pas être modifiée. La modification est possible uniquement jusqu'à 24h avant l'heure de réservation.")
        return redirect('mes_reservations')
    
    # Récupérer la salle pour afficher le calendrier
    salle = reservation.salle
    calendar_data = []
    
    
     # Préparer le calendrier de disponibilité pour la semaine
    today = date.today()
    
    if today.weekday() == 5:
        
        today += timedelta(days=2)
        
    elif today.weekday() == 6:
        
        today += timedelta(days=1)
   
    end_date = today + timedelta(days=7)
    
    # Récupérer toutes les réservations pour cette salle sur la période
    reservations = Reservation.objects.filter(
        salle=salle,
        date_res__gte=today,
        date_res__lte=end_date,
        etat='accepte'  # Seulement les réservations en attente ou acceptées
    ).exclude(id=reservation_id).order_by('date_res', 'heure_deb')
    
    # Créer les données du calendrier
    current_date = today
    while current_date <= end_date:
        # Filtrer les réservations pour ce jour
        day_reservations = reservations.filter(date_res=current_date)
       # Convertir chaque réservation en dict sérialisable
        serialized_reservations = []
        for res in day_reservations:
            serialized_reservations.append({
                'debut': res.heure_deb.strftime('%H:%M'),
                'fin': res.heure_fin.strftime('%H:%M'),
            })
        calendar_data.append({
            'date': current_date.strftime('%Y-%m-%d'),
            'reservations': serialized_reservations,
            })
        
        current_date += timedelta(days=1)
    
    if request.method == 'POST':
        form = ReservationForm(request.POST, instance=reservation)
        if form.is_valid():
            # Ne pas sauvegarder tout de suite
            reservation_modifiee = form.save(commit=False)
            
            # Vérifier la disponibilité
            if Reservation.est_disponible(
                salle_id=reservation_modifiee.salle.id,
                date_res=reservation_modifiee.date_res,
                heure_deb=reservation_modifiee.heure_deb,
                heure_fin=reservation_modifiee.heure_fin,
                reservation_id=reservation_id
            ):
                reservation_modifiee.utilisateur = request.user 
                reservation_modifiee.save()
                messages.success(request, "Votre réservation a été modifiée avec succès.")
                return redirect('mes_reservations')
            else:
                # Salle non disponible, afficher un message d'erreur
                messages.error(
                    request,
                    "La salle n'est pas disponible aux horaires sélectionnés."
                )
    else:
        form = ReservationForm(instance=reservation)
    
    context = {
        'form': form,
        'salle': salle,
        'calendar_data_json': mark_safe(json.dumps(calendar_data)),
        'mode_modification': True,
        'reservation': reservation
    }
    
    return render(request, 'Reservations/reserver.html', context)