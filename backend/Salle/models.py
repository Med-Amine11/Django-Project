from django.db import models
class Salle(models.Model):
    name = models.CharField(
        max_length=250,
        unique=True,
        verbose_name="Nom de la salle"
    )
    capacity = models.IntegerField(verbose_name="Capacité")
    description = models.TextField(verbose_name="Description")


    def __str__(self):
        return self.name
    

class Equipement(models.Model):
    name = models.CharField(
        max_length=250,
        unique=True,
        verbose_name="Nom de l'équipement"
    )
    salle = models.ForeignKey(
        Salle,
        on_delete=models.SET_NULL,
        null=True,
        related_name='equipements',
        verbose_name="Salle associée"
    )


    def __str__(self):
        return self.name