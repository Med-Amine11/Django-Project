# Generated by Django 4.2 on 2025-05-17 19:12

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Salle', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='Reservation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_res', models.DateField(verbose_name='Date de réservation')),
                ('heure_deb', models.TimeField(verbose_name='Heure de début')),
                ('heure_fin', models.TimeField(verbose_name='Heure de fin')),
                ('motif', models.TextField(verbose_name='Motif')),
                ('etat', models.CharField(choices=[('attente', 'En attente'), ('accepte', 'Acceptée'), ('refuse', 'Refusée'), ('annule', 'Annulée')], default='attente', max_length=10, verbose_name='État')),
                ('salle', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reservations', to='Salle.salle', verbose_name='Salle')),
                ('utilisateur', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reservations', to=settings.AUTH_USER_MODEL, verbose_name='Utilisateur')),
            ],
        ),
    ]
