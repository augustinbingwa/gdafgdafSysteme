# Generated by Django 2.0.7 on 2018-10-31 15:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mod_foncier', '0004_auto_20181029_0824'),
    ]

    operations = [
        migrations.AddField(
            model_name='foncierparcellepublique',
            name='usage',
            field=models.IntegerField(choices=[(0, 'Disponible'), (1, 'Activité'), (2, 'Panneau')], default=0),
        ),
    ]
