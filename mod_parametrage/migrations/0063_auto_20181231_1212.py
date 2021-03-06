# Generated by Django 2.0.7 on 2018-12-31 10:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mod_parametrage', '0062_auto_20181209_2145'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notification',
            name='entity',
            field=models.IntegerField(choices=[(8, 'Django-Model:AllocationPlaceMarche'), (10, 'Django-Model:FoncierParcelle'), (11, 'Django-Model:VehiculeActivite'), (5, 'Django-Model:AllocationEspacePublique'), (15, 'Django-Model:FoncierParcelleDuplicata'), (6, 'Django-Model:AllocationPanneauPublicitaire'), (7, 'Django-Model:PubliciteMurCloture'), (12, 'Django-Model:VehiculeActivite'), (13, 'Django-Model:VehiculeProprietaire'), (16, 'Django-Model:VehiculeActiviteDuplicata'), (17, 'Django-Model:VehiculeProprietaireDuplicata'), (3, 'Django-Model:ActiviteExceptionnel'), (1, 'Django-Model:Standard'), (2, 'Django-Model:Marche'), (18, 'Django-Model:BetailsPropriete'), (9, 'Location batiments municipaux'), (14, 'Django-Model:BaseActiviteDuplicata'), (4, 'Django-Model:VisiteSiteTouristique')], null=True),
        ),
    ]
