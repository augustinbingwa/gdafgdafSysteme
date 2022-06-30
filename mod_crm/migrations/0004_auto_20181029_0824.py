# Generated by Django 2.0.7 on 2018-10-29 06:24

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('mod_crm', '0003_contribuable_note'),
    ]

    operations = [
        migrations.AddField(
            model_name='contribuable',
            name='date_note',
            field=models.DateTimeField(null=True),
        ),
        migrations.AddField(
            model_name='contribuable',
            name='demande_annulation_validation',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='contribuable',
            name='reponse_note',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='contribuable',
            name='user_note',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='contribuable_requests_note', to=settings.AUTH_USER_MODEL),
        ),
    ]
