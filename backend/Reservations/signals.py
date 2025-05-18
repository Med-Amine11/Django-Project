# Reservations/signals.py

from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Reservation
from Notifications.models import Notification  # ajuste le chemin si nécessaire

@receiver(post_save, sender=Reservation)
def create_notification_on_reservation(sender, instance, created, **kwargs):
    utilisateur = instance.utilisateur
    salle = instance.salle

    if created:
        # Notification de création
        Notification.objects.create(
            utilisateur=utilisateur,
            reservation=instance,
            type="Réservation créée",
            message=f"Votre réservation pour la salle {salle.name} le {instance.date_res.strftime('%d/%m/%Y')} à {instance.heure_deb.strftime('%H:%M')} a été enregistrée.",
        )
    else:
        # Notification de modification
        Notification.objects.create(
            utilisateur=utilisateur,
            reservation=instance,
            type="Réservation modifiée",
            message=f"Votre réservation pour la salle {salle.name} le {instance.date_res.strftime('%d/%m/%Y')} a été modifiée.",
        )
