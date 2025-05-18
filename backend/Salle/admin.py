from django.contrib import admin
from .models import Salle , Equipement , Equipements_Salle

@admin.register(Salle) 
class SallesAdmin(admin.ModelAdmin) : 
    list_display = ['name'  ,'description' ,  'capacity']

@admin.register(Equipement)
class EquipementsAdmin(admin.ModelAdmin) : 
    list_display = ['name','description' , 'couleur' ,'Stock_Total' ]
    

@admin.register(Equipements_Salle)
class Equipements_Salle_Admin(admin.ModelAdmin) : 
    list_display = ['get_equipement_name', 'get_salle_name', 'quantite']

    def get_equipement_name(self, obj):
        return obj.equipement.name
    get_equipement_name.short_description = "Équipement"

    def get_salle_name(self, obj):
        return obj.salle.name
    get_salle_name.short_description = "Salle"