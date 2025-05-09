from django.db import models
from Users.models import Utilisateur 
from Reservations.models import Reservation 

class Notification(models.Model):
    utilisateur = models.ForeignKey(
        Utilisateur ,
        on_delete=models.CASCADE,
        related_name='notifications',
        verbose_name="Utilisateur"
    )
    reservation = models.ForeignKey(
        Reservation,
        on_delete=models.CASCADE,
        related_name='notifications',
        verbose_name="Reservation"
    )
    type = models.CharField(max_length=100, verbose_name="Type de notification")
    message = models.TextField(verbose_name="Message")
    date_envoi = models.DateTimeField(auto_now_add=True, verbose_name="Date d'envoi")
    
    
    def __str__(self):
        return f"Notification à {self.utilisateur.name} pour la réservation {self.reservation.id}"