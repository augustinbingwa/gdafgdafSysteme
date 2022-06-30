# Generated by Django 2.0.7 on 2018-10-29 06:24

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('mod_foncier', '0003_auto_20181026_1503'),
    ]

    operations = [
        migrations.AddField(
            model_name='foncierexpertise',
            name='date_note',
            field=models.DateTimeField(null=True),
        ),
        migrations.AddField(
            model_name='foncierexpertise',
            name='demande_annulation_validation',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='foncierexpertise',
            name='reponse_note',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='foncierexpertise',
            name='user_note',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='foncierexpertise_requests_note', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='foncierparcelle',
            name='date_note',
            field=models.DateTimeField(null=True),
        ),
        migrations.AddField(
            model_name='foncierparcelle',
            name='demande_annulation_validation',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='foncierparcelle',
            name='reponse_note',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='foncierparcelle',
            name='user_note',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='foncierparcelle_requests_note', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='foncierparcellepublique',
            name='date_note',
            field=models.DateTimeField(null=True),
        ),
        migrations.AddField(
            model_name='foncierparcellepublique',
            name='demande_annulation_validation',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='foncierparcellepublique',
            name='reponse_note',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='foncierparcellepublique',
            name='user_note',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='foncierparcellepublique_requests_note', to=settings.AUTH_USER_MODEL),
        ),
    ]
