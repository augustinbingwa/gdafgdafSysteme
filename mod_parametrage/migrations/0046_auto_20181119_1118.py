# Generated by Django 2.0.7 on 2018-11-19 09:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mod_parametrage', '0045_auto_20181115_1802'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notification',
            name='entity',
            field=models.IntegerField(choices=[(6, 'Django-Model:AllocationPanneauPublicitaire'), (3, 'Django-Model:ActiviteExceptionnel'), (9, 'Location batiments municipaux'), (17, 'Django-Model:VehiculeProprietaireDuplicata'), (4, 'Django-Model:VisiteSiteTouristique'), (8, 'Django-Model:AllocationPlaceMarche'), (18, 'Django-Model:BetailsPropriete'), (2, 'Django-Model:Marche'), (10, 'Django-Model:FoncierParcelle'), (1, 'Django-Model:Standard'), (11, 'Django-Model:VehiculeActivite'), (13, 'Django-Model:VehiculeProprietaire'), (15, 'Django-Model:FoncierParcelleDuplicata'), (7, 'Django-Model:PubliciteMurCloture'), (14, 'Django-Model:BaseActiviteDuplicata'), (12, 'Django-Model:VehiculeActivite'), (5, 'Django-Model:AllocationEspacePublique'), (16, 'Django-Model:VehiculeActiviteDuplicata')], null=True),
        ),
    ]
