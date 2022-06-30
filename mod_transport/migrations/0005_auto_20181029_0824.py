# Generated by Django 2.0.7 on 2018-10-29 06:24

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('mod_transport', '0004_auto_20181026_1503'),
    ]

    operations = [
        migrations.AddField(
            model_name='vehicule',
            name='date_note',
            field=models.DateTimeField(null=True),
        ),
        migrations.AddField(
            model_name='vehicule',
            name='demande_annulation_validation',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='vehicule',
            name='reponse_note',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='vehicule',
            name='user_note',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='vehicule_requests_note', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='vehiculeactivite',
            name='date_note',
            field=models.DateTimeField(null=True),
        ),
        migrations.AddField(
            model_name='vehiculeactivite',
            name='demande_annulation_validation',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='vehiculeactivite',
            name='reponse_note',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='vehiculeactivite',
            name='user_note',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='vehiculeactivite_requests_note', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='vehiculeactiviteduplicata',
            name='date_note',
            field=models.DateTimeField(null=True),
        ),
        migrations.AddField(
            model_name='vehiculeactiviteduplicata',
            name='demande_annulation_validation',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='vehiculeactiviteduplicata',
            name='reponse_note',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='vehiculeactiviteduplicata',
            name='user_note',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='vehiculeactiviteduplicata_requests_note', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='vehiculeproprietaire',
            name='date_note',
            field=models.DateTimeField(null=True),
        ),
        migrations.AddField(
            model_name='vehiculeproprietaire',
            name='demande_annulation_validation',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='vehiculeproprietaire',
            name='reponse_note',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='vehiculeproprietaire',
            name='user_note',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='vehiculeproprietaire_requests_note', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='vehiculeproprietaireduplicata',
            name='date_note',
            field=models.DateTimeField(null=True),
        ),
        migrations.AddField(
            model_name='vehiculeproprietaireduplicata',
            name='demande_annulation_validation',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='vehiculeproprietaireduplicata',
            name='reponse_note',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='vehiculeproprietaireduplicata',
            name='user_note',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='vehiculeproprietaireduplicata_requests_note', to=settings.AUTH_USER_MODEL),
        ),
    ]