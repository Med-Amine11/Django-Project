from django.db import models
from django.forms import ValidationError
from Salle.models import Salle
from Users.models import Utilisateur
from datetime import date, datetime, timedelta

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
      return f'{self.id} - {self.utilisateur. first_name} {self.utilisateur.last_name}'
  
    def clean(self):
        super().clean()  # Vérifie les contraintes de base
        # Empêcher les admins de réserver
        if hasattr(self, 'utilisateur') and self.utilisateur and (self.utilisateur.is_staff or self.utilisateur.is_superuser):
             raise ValidationError("Les administrateurs ne sont pas autorisés à faire des réservations.")

    @classmethod
    def est_disponible(cls, salle_id, date_res, heure_deb, heure_fin, reservation_id=None):
        """
        Vérifie si une salle est disponible à la date et heures spécifiées.
        
        Args:
            salle_id: ID de la salle à vérifier
            date_res: Date de réservation
            heure_deb: Heure de début
            heure_fin: Heure de fin
            reservation_id: ID de la réservation actuelle (pour exclure lors d'une modification)
            
        Returns:
            bool: True si la salle est disponible, False sinon
        """
        # Recherche des réservations qui se chevauchent
        # Une réservation se chevauche si elle n'est pas entièrement avant ou entièrement après
         # Vérification des limites horaires
        reservations_chevauchantes = cls.objects.filter(
            salle_id=salle_id,
            date_res=date_res,
            # Exclure les réservations refusées ou annulées
            etat__in=['attente', 'accepte']
        ).exclude(
            # Exclure les réservations qui se terminent avant le début de la nouvelle
            heure_fin__lte=heure_deb
        ).exclude(
            # Exclure les réservations qui commencent après la fin de la nouvelle
            heure_deb__gte=heure_fin
        ).exclude(id = reservation_id) 
        # La salle est disponible s'il n'y a pas de réservations qui se chevauchent
        return not reservations_chevauchantes.exists()

    @classmethod
    def utilisateur_a_trop_de_reservations(cls, id):
        """
        Vérifie si l'utilisateur a déjà 3 réservations actives (en attente ou acceptées)
        
        Args:
            utilisateur_id: ID de l'utilisateur à vérifier
            reservation_id: ID de la réservation actuelle à exclure (pour les modifications)
            
        Returns:
            bool: True si l'utilisateur a déjà 3 réservations actives
        """
        reservations = cls.objects.filter(
            utilisateur_id=id,
            etat = 'accepte'  ,
            heure_deb__gt= date.today().strftime('%H:%M') 
        )
        return reservations.count() >= 3
    
    def peut_annuler(self):
        """
        Vérifie si la réservation peut être annulée (jusqu'à 24h avant)
        
        Returns:
            bool: True si la réservation peut être annulée
        """
        if self.etat  == 'attente'  :
            return True
        elif self.etat == 'accepte' :
            # Calculer la date et l'heure de la réservation
           date_heure_reservation = datetime.combine(self.date_res, self.heure_deb)
        
            # Calculer la date et l'heure actuelle
           now = datetime.now()
        
           # Calculer la différence
           diff = date_heure_reservation - now
        
          # Vérifier si la différence est d'au moins 24 heures
           return diff > timedelta(hours=24)
    
    def peut_modifier(self):
        """
        Vérifie si la réservation peut être modifiée (mêmes conditions que l'annulation)
        
        Returns:
            bool: True si la réservation peut être modifiée
        """
        return self.peut_annuler()