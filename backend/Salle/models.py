import shutil
from autoslug import AutoSlugField 
from django.db import models 
import os
from django.utils.text import slugify 
from django.db.models.signals import pre_save , post_delete , post_save 
from django.dispatch import receiver 
from django.core.exceptions import ValidationError
def salle_image_path(instance, filename):
    return os.path.join('Salle', slugify(instance.name), filename)

def equipement_image_path(instance , filename) : 
    return os.path.join('Equipement' , slugify(instance.name)  , filename)

class Salle(models.Model):
    name = models.CharField(
        max_length=250,
        unique=True,
        verbose_name="Nom de la salle" , 
        blank=False
    )
    slug =  AutoSlugField(populate_from='name', unique=True)
    capacity = models.PositiveIntegerField(verbose_name="Capacité" ) 
    description = models.TextField(verbose_name="Description")
    image = models.ImageField(upload_to=salle_image_path)

    def __str__(self):
        return self.name
    
@receiver(pre_save, sender=Salle) 
def handle_salle_change(sender, instance, **kwargs): 
    
    if instance.pk: 
        ancienne_salle = Salle.objects.get(pk=instance.pk) 
        nouveau_slug = slugify(instance.name)
        
        # Supprimer l'ancienne image si elle a été changée
        if ancienne_salle.image != instance.image and os.path.isfile(ancienne_salle.image.path): 
            os.remove(ancienne_salle.image.path) 
        
        # Renommer le dossier si le nom a changé
        if ancienne_salle.slug != nouveau_slug:
            old_dir = f"media/Salle/{ancienne_salle.slug}"
            new_dir = f"media/Salle/{nouveau_slug}"
            
            # Renommer le dossier s'il existe
            if os.path.isdir(old_dir):
                os.rename(old_dir, new_dir)
                
            # Mettre à jour le slug
            instance.slug = nouveau_slug

@receiver(post_delete, sender=Salle)
def handle_salle_delete(sender, instance, **kwargs):
    
    # Supprimer l'image si elle existe
    if os.path.isfile(instance.image.path):
        os.remove(instance.image.path)
    
    # Supprimer le dossier complet
    salle_dir = f"media/Salle/{instance.slug}"
    if os.path.isdir(salle_dir):
        shutil.rmtree(salle_dir)
        
        
@receiver(post_save , sender = Salle)
def handle_salle_change_images(sender, instance , **kwargs) :
    dossier = os.path.join('media', 'Salle', instance.slug)
    
    if os.path.isdir(dossier):
        image_actuelle = os.path.basename(instance.image.name)

        for fichier in os.listdir(dossier):
            chemin_fichier = os.path.join(dossier, fichier)
            if fichier != image_actuelle :
                os.remove(chemin_fichier)
        
class Equipement(models.Model):
    name = models.CharField(
        max_length=250,
        unique=True,
        verbose_name="Nom de l'équipement" , 
        blank=False
    )
    slug = AutoSlugField(populate_from='name', unique=True)
    couleur = models.CharField(max_length=150 , verbose_name="Couleur de l'equipement")
    description = models.CharField(max_length=255, blank = True,verbose_name="Description")
    Stock_Total = models.PositiveIntegerField(verbose_name="Stock total")   
    image = models.ImageField(upload_to=equipement_image_path , verbose_name='Image' ) 
    
    def __str__(self):
        return self.name
    


@receiver(pre_save , sender = Equipement) 
def handle_equipement_change(sender , instance , **kwargs) : 
    if instance.pk : 
        equipement_modifiee = Equipement.objects.get(pk = instance.pk) 
        
        nouveau_slug = slugify(instance.name)
        
        if equipement_modifiee.image != instance.image and  os.path.isfile(equipement_modifiee.image.path)  : 
            os.remove(equipement_modifiee.image.path) 
       
        old_dir = f"media/Equipement/{equipement_modifiee.slug}"
        new_dir = f"media/Equipement/{nouveau_slug}"
        
        if os.path.isdir(old_dir) : 
            os.rename(old_dir ,new_dir)
        
        instance.slug = nouveau_slug 
    
@receiver(post_delete ,sender=Equipement ) 
def handle_equipement_deleted(sender , instance , **kwargs) : 
    if os.path.isfile(instance.image.path) : 
        os.remove(instance.image.path)
    slug = slugify(instance.name)
    if os.path.isdir(f"media/Equipement/{slug}") : 
        shutil.rmtree(f"media/Equipement/{slug}")

@receiver(post_save , sender = Equipement)
def handle_Equipement_change_images(sender , instance , **kwargs) : 
    dossier  = os.path.join("media","Equipement" , instance.slug)
    
    if os.path.isdir(dossier) : 
        
        image_name = os.path.basename(instance.image.name)
        
        for fichier in os.listdir(dossier) : 
            
            chemin_fichier = os.path.join(dossier, fichier)
            
            if fichier != image_name : 
                
                os.remove(chemin_fichier)
                
                
class Equipements_Salle(models.Model) : 
    salle = models.ForeignKey(Salle, on_delete=models.CASCADE, related_name='equipements_salle')
    equipement = models.ForeignKey(Equipement, on_delete=models.CASCADE, related_name='salles')
    quantite = models.PositiveIntegerField(verbose_name="Quantite dans la salle")
    
    
    def __str__(self):
        return f"{self.equipement.name} ({self.quantite}) dans {self.salle.name}"


@receiver(pre_save, sender=Equipements_Salle)
def check_quantite_vs_stock(sender, instance, **kwargs):
    if instance.quantite > instance.equipement.Stock_Total:
        raise ValidationError("La quantité dépasse le stock total disponible.")