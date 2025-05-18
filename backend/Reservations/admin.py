from django.contrib import admin
from .models import Reservation

@admin.register(Reservation)
class ReservationsAdmin(admin.ModelAdmin):
    list_display = ['get_utilisateur_nom','get_utilisateur_prenom', 'get_salle_nom' ,'date_res', 'heure_deb', 'heure_fin', 'motif','etat']  
    @admin.display(description='Nom Utilisateur')
    def get_utilisateur_nom(self, obj):
        return obj.utilisateur.last_name
    
    @admin.display(description='Prénom Utilisateur')
    def get_utilisateur_prenom(self, obj):
        return obj.utilisateur.first_name
    @admin.display(description='Nom de la salle')
    def get_salle_nom(self,obj) : 
        return obj.salle.name 
