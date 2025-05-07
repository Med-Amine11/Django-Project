from django.db import models
from django.contrib.auth.models import AbstractUser

class Utilisateur(AbstractUser):
    adresse = models.CharField(max_length=255)
    numero_tele = models.CharField(max_length=15)
    type_utilisateur = models.CharField(max_length=50, choices=[
        ('admin', 'Admin'),
        ('employé', 'Employe'),
        ('étudiant', 'Etudiant'),
        ('formateur', 'Formateur'),
    ])
    
    def __str__(self):
        return f'{self.nom}  {self.prenom}'

    
    
    