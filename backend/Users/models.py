from django.db import models
from django.contrib.auth.models import AbstractUser

class Utilisateur(AbstractUser):
    adresse = models.CharField(max_length=255)
    numero_tele = models.CharField(max_length=15)
    
    def __str__(self):
        return f'{self.first_name}  {self.last_name}'

    
    
    