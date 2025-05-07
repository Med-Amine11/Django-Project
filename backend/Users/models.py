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
    # Définir des related_name pour éviter les conflits avec les groupes et les permissions
    groups = models.ManyToManyField(
        'auth.Group', related_name='utilisateurs_set', blank=True)
    user_permissions = models.ManyToManyField(
        'auth.Permission', related_name='utilisateurs_set', blank=True)
    def __str__(self):
        return f'{self.nom}  {self.prenom}'

    
    
    