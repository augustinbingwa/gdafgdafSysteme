# Generated by Django 2.0.7 on 2018-10-19 10:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mod_parametrage', '0002_auto_20181012_1512'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notification',
            name='entity',
            field=models.IntegerField(choices=[(3, 'Django-Model:ActiviteExceptionnel'), (6, 'Django-Model:AllocationPanneauPublicitaire'), (16, 'Django-Model:VehiculeActiviteDuplicata'), (17, 'Django-Model:VehiculeProprietaireDuplicata'), (14, 'Django-Model:BaseActiviteDuplicata'), (9, 'Location batiments municipaux'), (12, 'Django-Model:VehiculeActivite'), (11, 'Django-Model:VehiculeActivite'), (13, 'Django-Model:VehiculeProprietaire'), (5, 'Django-Model:AllocationEspacePublique'), (18, 'Django-Model:BetailsPropriete'), (8, 'Django-Model:AllocationPlaceMarche'), (2, 'Django-Model:Marche'), (10, 'Django-Model:FoncierParcelle'), (15, 'Django-Model:FoncierParcelleDuplicata'), (7, 'Django-Model:PubliciteMurCloture'), (1, 'Django-Model:Standard'), (4, 'Django-Model:VisiteSiteTouristique')], null=True),
        ),
    ]
