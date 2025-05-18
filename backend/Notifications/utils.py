from .models import Notification

def creer_notification(utilisateur, reservation, type_notif, message):
    Notification.objects.create(
        utilisateur=utilisateur,
        reservation=reservation,
        type=type_notif,
        message=message
    )

def creer_notification_modification(reservation):
    utilisateur = reservation.utilisateur
    salle = reservation.salle
    message = (
        f"Votre réservation pour la salle {salle.name} a été modifiée avec succès. "
        f"Nouveaux horaires : le {reservation.date_res.strftime('%d/%m/%Y')} "
        f"de {reservation.heure_deb.strftime('%H:%M')} à {reservation.heure_fin.strftime('%H:%M')}."
    )
    creer_notification(utilisateur, reservation, "Réservation modifiée", message)
