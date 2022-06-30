# Generated by Django 2.0.7 on 2018-12-07 09:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mod_parametrage', '0055_auto_20181205_1637'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notification',
            name='entity',
            field=models.IntegerField(choices=[(16, 'Django-Model:VehiculeActiviteDuplicata'), (6, 'Django-Model:AllocationPanneauPublicitaire'), (14, 'Django-Model:BaseActiviteDuplicata'), (10, 'Django-Model:FoncierParcelle'), (12, 'Django-Model:VehiculeActivite'), (1, 'Django-Model:Standard'), (2, 'Django-Model:Marche'), (15, 'Django-Model:FoncierParcelleDuplicata'), (17, 'Django-Model:VehiculeProprietaireDuplicata'), (18, 'Django-Model:BetailsPropriete'), (8, 'Django-Model:AllocationPlaceMarche'), (9, 'Location batiments municipaux'), (11, 'Django-Model:VehiculeActivite'), (13, 'Django-Model:VehiculeProprietaire'), (3, 'Django-Model:ActiviteExceptionnel'), (7, 'Django-Model:PubliciteMurCloture'), (5, 'Django-Model:AllocationEspacePublique'), (4, 'Django-Model:VisiteSiteTouristique')], null=True),
        ),
    ]