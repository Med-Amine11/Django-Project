from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from datetime import date, timedelta, datetime
from .forms import ReservationForm
from .models import Reservation
from Salle.models import Salle

@login_required
def effectuer_reservation(request):
    # Vérifier si l'utilisateur a déjà 3 réservations actives
    if Reservation.utilisateur_a_trop_de_reservations(request.user.id):
        messages.error(request, "Vous avez déjà 3 réservations actives. Vous ne pouvez pas avoir plus de 3 réservations à la fois.")
        return redirect('mes_reservations')
    
    # Récupérer l'ID de la salle depuis l'URL
    salle_id = request.GET.get('salle_id')
    
    # Si un ID de salle est fourni, récupérer cette salle ou retourner une erreur 404
    salle = None
    calendar_data = []
    
    if salle_id:
        salle = get_object_or_404(Salle, id=salle_id)
        
        # Préparer le calendrier de disponibilité pour la semaine
        today = date.today()
        end_date = today + timedelta(days=7)
        
        # Récupérer toutes les réservations pour cette salle sur la période
        reservations = Reservation.objects.filter(
            salle=salle,
            date_res__gte=today,
            date_res__lte=end_date,
            etat__in=['attente', 'accepte']  # Seulement les réservations en attente ou acceptées
        ).order_by('date_res', 'heure_deb')
        
        # Créer les données du calendrier
        current_date = today
        while current_date <= end_date:
            # Filtrer les réservations pour ce jour
            day_reservations = reservations.filter(date_res=current_date)
            
            calendar_data.append({
                'date': current_date,
                'weekday': current_date.strftime('%A'),
                'reservations': day_reservations,
                'is_today': current_date == today
            })
            
            current_date += timedelta(days=1)
    
    if request.method == 'POST':
        form = ReservationForm(request.POST)
        if form.is_valid():
            # Ne pas sauvegarder tout de suite
            reservation = form.save(commit=False)
            reservation.utilisateur = request.user
            
            # Vérifier la disponibilité
            if Reservation.est_disponible(
                salle_id=reservation.salle.id,
                date_res=reservation.date_res,
                heure_deb=reservation.heure_deb,
                heure_fin=reservation.heure_fin
            ):
                # Salle disponible, enregistrer la réservation
                reservation.save()
                messages.success(request, "Votre réservation a été effectuée avec succès et est en attente de validation.")
                return redirect('mes_reservations')
            else:
                # Salle non disponible, afficher un message d'erreur
                messages.error(request, "La salle n'est pas disponible aux horaires sélectionnés.")
    else:
        # Pour un nouveau formulaire, on prérempli la salle si elle est fournie
        initial = {'salle': salle_id} if salle_id else {}
        form = ReservationForm(initial=initial)
    
    context = {
        'form': form,
        'salle': salle,
        'calendar_data': calendar_data,
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
        # Mettre à jour l'état de la réservation
        reservation.etat = 'annule'
        reservation.save()
        messages.success(request, "Votre réservation a été annulée avec succès.")
        return redirect('mes_reservations')
    
    context = {
        'reservation': reservation
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
    end_date = today + timedelta(days=7)
    
    # Récupérer toutes les réservations pour cette salle sur la période
    reservations = Reservation.objects.filter(
        salle=salle,
        date_res__gte=today,
        date_res__lte=end_date,
        etat__in=['attente', 'accepte']  # Seulement les réservations en attente ou acceptées
    ).exclude(id=reservation_id).order_by('date_res', 'heure_deb')
    
    # Créer les données du calendrier
    current_date = today
    while current_date <= end_date:
        # Filtrer les réservations pour ce jour
        day_reservations = reservations.filter(date_res=current_date)
        
        calendar_data.append({
            'date': current_date,
            'weekday': current_date.strftime('%A'),
            'reservations': day_reservations,
            'is_today': current_date == today
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
                # Salle disponible, enregistrer la réservation
                reservation_modifiee.save()
                messages.success(request, "Votre réservation a été modifiée avec succès.")
                return redirect('mes_reservations')
            else:
                # Salle non disponible, afficher un message d'erreur
                messages.error(request, "La salle n'est pas disponible aux horaires sélectionnés.")
    else:
        form = ReservationForm(instance=reservation)
    
    context = {
        'form': form,
        'salle': salle,
        'calendar_data': calendar_data,
        'mode_modification': True,
        'reservation': reservation
    }
    
    return render(request, 'Reservations/reserver.html', context)