# Generated by Django 2.0.7 on 2018-11-15 12:38

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('mod_activite', '0019_auto_20181113_1008'),
    ]

    operations = [
        migrations.AddField(
            model_name='activiteexceptionnelle',
            name='date_cancel',
            field=models.DateTimeField(null=True),
        ),
        migrations.AddField(
            model_name='activiteexceptionnelle',
            name='user_cancel',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='activiteexceptionnelle_requests_cancel', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='allocationespacepublique',
            name='date_cancel',
            field=models.DateTimeField(null=True),
        ),
        migrations.AddField(
            model_name='allocationespacepublique',
            name='user_cancel',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='allocationespacepublique_requests_cancel', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='allocationpanneaupublicitaire',
            name='date_cancel',
            field=models.DateTimeField(null=True),
        ),
        migrations.AddField(
            model_name='allocationpanneaupublicitaire',
            name='user_cancel',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='allocationpanneaupublicitaire_requests_cancel', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='allocationplacemarche',
            name='date_cancel',
            field=models.DateTimeField(null=True),
        ),
        migrations.AddField(
            model_name='allocationplacemarche',
            name='user_cancel',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='allocationplacemarche_requests_cancel', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='arretservice',
            name='date_cancel',
            field=models.DateTimeField(null=True),
        ),
        migrations.AddField(
            model_name='arretservice',
            name='user_cancel',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='arretservice_requests_cancel', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='baseactivite',
            name='date_cancel',
            field=models.DateTimeField(null=True),
        ),
        migrations.AddField(
            model_name='baseactivite',
            name='user_cancel',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='baseactivite_requests_cancel', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='publicitemurcloture',
            name='date_cancel',
            field=models.DateTimeField(null=True),
        ),
        migrations.AddField(
            model_name='publicitemurcloture',
            name='user_cancel',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='publicitemurcloture_requests_cancel', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='visitesitetouristique',
            name='date_cancel',
            field=models.DateTimeField(null=True),
        ),
        migrations.AddField(
            model_name='visitesitetouristique',
            name='user_cancel',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='visitesitetouristique_requests_cancel', to=settings.AUTH_USER_MODEL),
        ),
    ]
