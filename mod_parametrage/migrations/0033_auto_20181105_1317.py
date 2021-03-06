# Generated by Django 2.0.7 on 2018-11-05 11:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mod_parametrage', '0032_auto_20181105_1029'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notification',
            name='entity',
            field=models.IntegerField(choices=[(18, 'Django-Model:BetailsPropriete'), (13, 'Django-Model:VehiculeProprietaire'), (7, 'Django-Model:PubliciteMurCloture'), (6, 'Django-Model:AllocationPanneauPublicitaire'), (16, 'Django-Model:VehiculeActiviteDuplicata'), (12, 'Django-Model:VehiculeActivite'), (10, 'Django-Model:FoncierParcelle'), (8, 'Django-Model:AllocationPlaceMarche'), (15, 'Django-Model:FoncierParcelleDuplicata'), (5, 'Django-Model:AllocationEspacePublique'), (3, 'Django-Model:ActiviteExceptionnel'), (17, 'Django-Model:VehiculeProprietaireDuplicata'), (2, 'Django-Model:Marche'), (14, 'Django-Model:BaseActiviteDuplicata'), (11, 'Django-Model:VehiculeActivite'), (4, 'Django-Model:VisiteSiteTouristique'), (1, 'Django-Model:Standard'), (9, 'Location batiments municipaux')], null=True),
        ),
    ]
