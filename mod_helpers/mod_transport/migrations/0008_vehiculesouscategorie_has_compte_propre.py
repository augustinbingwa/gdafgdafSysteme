# Generated by Django 2.0.7 on 2019-02-20 10:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mod_transport', '0007_auto_20190213_1056'),
    ]

    operations = [
        migrations.AddField(
            model_name='vehiculesouscategorie',
            name='has_compte_propre',
            field=models.BooleanField(default=False, verbose_name='Compte propre (sans activité mais qui paierait seulement le droit de stationnement)'),
        ),
    ]
