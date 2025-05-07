from django.db import models
from Salle.models import Salle
from Users.models import Utilisateur
# Create your models here.

class Reservation(models.Model):
    ETAT_CHOICES = [
        ('attente', 'En attente'),
        ('accepte', 'Acceptée'),
        ('refuse', 'Refusée'),
    ]

    utilisateur = models.ForeignKey(
        Utilisateur,
        on_delete=models.CASCADE,
        related_name='reservations',
        verbose_name="Utilisateur"
    )
    salle = models.ForeignKey(
        Salle,
        on_delete=models.CASCADE,
        related_name='reservations',
        verbose_name="Salle"
    )
    date_res = models.DateField(verbose_name="Date de réservation")
    heure_deb = models.TimeField(verbose_name="Heure de début")
    heure_fin = models.TimeField(verbose_name="Heure de fin")
    motif = models.TextField(verbose_name="Motif")
    etat = models.CharField(
        max_length=10,
        choices=ETAT_CHOICES,
        default='attente',
        verbose_name="État"
    )
    
    def __str__(self):
        return f"{self.utilisateur.first_name} - {self.salle.name} ({self.date_res} {self.heure_deb}-{self.heure_fin}) - ({self.etat})"