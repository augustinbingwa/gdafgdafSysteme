# Generated by Django 2.0.7 on 2018-12-05 14:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mod_parametrage', '0053_auto_20181205_1232'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notification',
            name='entity',
            field=models.IntegerField(choices=[(3, 'Django-Model:ActiviteExceptionnel'), (1, 'Django-Model:Standard'), (15, 'Django-Model:FoncierParcelleDuplicata'), (10, 'Django-Model:FoncierParcelle'), (16, 'Django-Model:VehiculeActiviteDuplicata'), (5, 'Django-Model:AllocationEspacePublique'), (11, 'Django-Model:VehiculeActivite'), (8, 'Django-Model:AllocationPlaceMarche'), (13, 'Django-Model:VehiculeProprietaire'), (18, 'Django-Model:BetailsPropriete'), (9, 'Location batiments municipaux'), (17, 'Django-Model:VehiculeProprietaireDuplicata'), (14, 'Django-Model:BaseActiviteDuplicata'), (2, 'Django-Model:Marche'), (7, 'Django-Model:PubliciteMurCloture'), (6, 'Django-Model:AllocationPanneauPublicitaire'), (12, 'Django-Model:VehiculeActivite'), (4, 'Django-Model:VisiteSiteTouristique')], null=True),
        ),
    ]
