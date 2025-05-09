from django.contrib import admin
from .models import Salle , Equipement

@admin.register(Salle) 
class SallesAdmin(admin.ModelAdmin) : 
    list_display = ['name'  ,'slug' ,  'capacity']

@admin.register(Equipement)
class EquipementsAdmin(admin.ModelAdmin) : 
    list_display = ['name' ]
