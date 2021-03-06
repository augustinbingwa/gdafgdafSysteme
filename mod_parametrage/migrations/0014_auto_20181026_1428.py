# Generated by Django 2.0.7 on 2018-10-26 12:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mod_parametrage', '0013_auto_20181024_1134'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notification',
            name='entity',
            field=models.IntegerField(choices=[(16, 'Django-Model:VehiculeActiviteDuplicata'), (10, 'Django-Model:FoncierParcelle'), (7, 'Django-Model:PubliciteMurCloture'), (1, 'Django-Model:Standard'), (8, 'Django-Model:AllocationPlaceMarche'), (18, 'Django-Model:BetailsPropriete'), (6, 'Django-Model:AllocationPanneauPublicitaire'), (11, 'Django-Model:VehiculeActivite'), (4, 'Django-Model:VisiteSiteTouristique'), (3, 'Django-Model:ActiviteExceptionnel'), (15, 'Django-Model:FoncierParcelleDuplicata'), (17, 'Django-Model:VehiculeProprietaireDuplicata'), (9, 'Location batiments municipaux'), (13, 'Django-Model:VehiculeProprietaire'), (12, 'Django-Model:VehiculeActivite'), (14, 'Django-Model:BaseActiviteDuplicata'), (2, 'Django-Model:Marche'), (5, 'Django-Model:AllocationEspacePublique')], null=True),
        ),
    ]
