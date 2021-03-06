# Generated by Django 2.0.7 on 2018-10-23 23:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mod_parametrage', '0010_auto_20181023_2356'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notification',
            name='entity',
            field=models.IntegerField(choices=[(12, 'Django-Model:VehiculeActivite'), (8, 'Django-Model:AllocationPlaceMarche'), (6, 'Django-Model:AllocationPanneauPublicitaire'), (9, 'Location batiments municipaux'), (5, 'Django-Model:AllocationEspacePublique'), (17, 'Django-Model:VehiculeProprietaireDuplicata'), (2, 'Django-Model:Marche'), (7, 'Django-Model:PubliciteMurCloture'), (16, 'Django-Model:VehiculeActiviteDuplicata'), (3, 'Django-Model:ActiviteExceptionnel'), (13, 'Django-Model:VehiculeProprietaire'), (15, 'Django-Model:FoncierParcelleDuplicata'), (1, 'Django-Model:Standard'), (11, 'Django-Model:VehiculeActivite'), (10, 'Django-Model:FoncierParcelle'), (14, 'Django-Model:BaseActiviteDuplicata'), (18, 'Django-Model:BetailsPropriete'), (4, 'Django-Model:VisiteSiteTouristique')], null=True),
        ),
    ]
