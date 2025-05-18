from django import forms
from .models import Reservation
from django.core.exceptions import ValidationError
import datetime

class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ['salle', 'date_res', 'heure_deb', 'heure_fin', 'motif']
        widgets = {
            'salle': forms.Select(attrs={'class': 'form-control', 'id': 'id_salle'}),
            'date_res': forms.DateInput(attrs={'type': 'date', 'class': 'form-control', 'id': 'id_date_res'}),
            'heure_deb': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control', 'id': 'id_heure_deb'}),
            'heure_fin': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control', 'id': 'id_heure_fin'}),
            'motif': forms.Textarea(attrs={'rows': 4, 'class': 'form-control', 'id': 'id_motif'})
        }
        
    def clean(self):
        cleaned_data = super().clean()
        date_res = cleaned_data.get('date_res')
        heure_deb = cleaned_data.get('heure_deb')
        heure_fin = cleaned_data.get('heure_fin')
        
        # Vérifications de base
        today = datetime.date.today()
        
        # Vérifier que la date est dans le futur
        if date_res and date_res < today:
            raise ValidationError("Impossible de réserver une date passée.")
        
        # Interdire les réservations le week-end
        if date_res and date_res.weekday() >= 5:  # 5 = samedi, 6 = dimanche
            raise ValidationError("Les réservations ne sont pas autorisées le week-end (samedi ou dimanche).")
        
        # La réservation doit être effectuée au moins 7 jours à l'avance
        if date_res:
            if (date_res - today).days > 7:
                raise ValidationError("Les réservations doivent être faites au moins 7 jours à l'avance.")
            
        # Vérifier que l'heure de fin est après l'heure de début
        if heure_deb and heure_fin and heure_fin <= heure_deb:
            raise ValidationError("L'heure de fin doit être après l'heure de début.")
        
        # Vérifier que l'heure de réservation est raisonnable (ex: entre 8h et 22h)
        if heure_deb and heure_fin  and (heure_deb.hour < 8 or heure_deb.hour >= 22):
            raise ValidationError("Les réservations sont possibles uniquement entre 8h et 22h.")
        
        # Durée minimale et maximale
        if heure_deb and heure_fin:
            debut_minutes = heure_deb.hour * 60 + heure_deb.minute
            fin_minutes = heure_fin.hour * 60 + heure_fin.minute
            duree_minutes = fin_minutes - debut_minutes
            
            if duree_minutes < 30:
                raise ValidationError("La durée minimale de réservation est de 30 minutes.")
            
            if duree_minutes > 480:  # 8 heures max
                raise ValidationError("La durée maximale de réservation est de 8 heures.")
        
        # Vérifier que la réservation est au moins 24h dans le futur
        if date_res and heure_deb:
            date_heure_reservation = datetime.datetime.combine(date_res, heure_deb)
            now = datetime.datetime.now()
            diff = date_heure_reservation - now
            
            if diff < datetime.timedelta(hours=24):
                raise ValidationError("Les réservations doivent être effectuées au moins 24h à l'avance.")
        
        return cleaned_data