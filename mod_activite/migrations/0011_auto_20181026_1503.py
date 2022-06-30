# Generated by Django 2.0.7 on 2018-10-26 13:03

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('mod_activite', '0010_auto_20181026_1428'),
    ]

    operations = [
        migrations.AddField(
            model_name='activiteexceptionnelle',
            name='date_ecriture',
            field=models.DateTimeField(null=True),
        ),
        migrations.AddField(
            model_name='activiteexceptionnelle',
            name='user_ecriture',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='activiteexceptionnelle_requests_ecriture', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='allocationespacepublique',
            name='date_ecriture',
            field=models.DateTimeField(null=True),
        ),
        migrations.AddField(
            model_name='allocationespacepublique',
            name='user_ecriture',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='allocationespacepublique_requests_ecriture', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='allocationpanneaupublicitaire',
            name='date_ecriture',
            field=models.DateTimeField(null=True),
        ),
        migrations.AddField(
            model_name='allocationpanneaupublicitaire',
            name='user_ecriture',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='allocationpanneaupublicitaire_requests_ecriture', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='allocationplacemarche',
            name='date_ecriture',
            field=models.DateTimeField(null=True),
        ),
        migrations.AddField(
            model_name='allocationplacemarche',
            name='user_ecriture',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='allocationplacemarche_requests_ecriture', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='baseactivite',
            name='date_ecriture',
            field=models.DateTimeField(null=True),
        ),
        migrations.AddField(
            model_name='baseactivite',
            name='user_ecriture',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='baseactivite_requests_ecriture', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='publicitemurcloture',
            name='date_ecriture',
            field=models.DateTimeField(null=True),
        ),
        migrations.AddField(
            model_name='publicitemurcloture',
            name='user_ecriture',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='publicitemurcloture_requests_ecriture', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='visitesitetouristique',
            name='date_ecriture',
            field=models.DateTimeField(null=True),
        ),
        migrations.AddField(
            model_name='visitesitetouristique',
            name='user_ecriture',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='visitesitetouristique_requests_ecriture', to=settings.AUTH_USER_MODEL),
        ),
    ]
