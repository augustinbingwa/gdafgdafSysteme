# Generated by Django 2.0.7 on 2019-01-12 09:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mod_parametrage', '0076_auto_20190111_0925'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notification',
            name='entity',
            field=models.IntegerField(choices=[(3, 'Django-Model:ActiviteExceptionnel'), (6, 'Django-Model:AllocationPanneauPublicitaire'), (18, 'Django-Model:BetailsPropriete'), (11, 'Django-Model:VehiculeActivite'), (10, 'Django-Model:FoncierParcelle'), (7, 'Django-Model:PubliciteMurCloture'), (1, 'Django-Model:Standard'), (5, 'Django-Model:AllocationEspacePublique'), (8, 'Django-Model:AllocationPlaceMarche'), (13, 'Django-Model:VehiculeProprietaire'), (16, 'Django-Model:VehiculeActiviteDuplicata'), (9, 'Location batiments municipaux'), (12, 'Django-Model:VehiculeActivite'), (4, 'Django-Model:VisiteSiteTouristique'), (15, 'Django-Model:FoncierParcelleDuplicata'), (2, 'Django-Model:Marche'), (17, 'Django-Model:VehiculeProprietaireDuplicata'), (14, 'Django-Model:BaseActiviteDuplicata')], null=True),
        ),
    ]
