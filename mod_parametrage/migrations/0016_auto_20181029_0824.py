# Generated by Django 2.0.7 on 2018-10-29 06:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mod_parametrage', '0015_auto_20181026_1503'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notification',
            name='entity',
            field=models.IntegerField(choices=[(14, 'Django-Model:BaseActiviteDuplicata'), (4, 'Django-Model:VisiteSiteTouristique'), (2, 'Django-Model:Marche'), (9, 'Location batiments municipaux'), (5, 'Django-Model:AllocationEspacePublique'), (11, 'Django-Model:VehiculeActivite'), (13, 'Django-Model:VehiculeProprietaire'), (7, 'Django-Model:PubliciteMurCloture'), (1, 'Django-Model:Standard'), (10, 'Django-Model:FoncierParcelle'), (18, 'Django-Model:BetailsPropriete'), (17, 'Django-Model:VehiculeProprietaireDuplicata'), (12, 'Django-Model:VehiculeActivite'), (16, 'Django-Model:VehiculeActiviteDuplicata'), (6, 'Django-Model:AllocationPanneauPublicitaire'), (15, 'Django-Model:FoncierParcelleDuplicata'), (8, 'Django-Model:AllocationPlaceMarche'), (3, 'Django-Model:ActiviteExceptionnel')], null=True),
        ),
    ]
