# Generated by Django 2.0.7 on 2020-05-05 14:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mod_parametrage', '0106_auto_20200218_2001'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notification',
            name='entity',
            field=models.PositiveSmallIntegerField(choices=[(6, 'Django-Model:AllocationPanneauPublicitaire'), (14, 'Django-Model:BaseActiviteDuplicata'), (3, 'Django-Model:ActiviteExceptionnel'), (18, 'Django-Model:BetailsPropriete'), (2, 'Django-Model:Marche'), (1, 'Django-Model:Standard'), (5, 'Django-Model:AllocationEspacePublique'), (10, 'Django-Model:FoncierParcelle'), (7, 'Django-Model:PubliciteMurCloture'), (8, 'Django-Model:AllocationPlaceMarche'), (15, 'Django-Model:FoncierParcelleDuplicata'), (11, 'Django-Model:VehiculeActivite'), (13, 'Django-Model:VehiculeProprietaire'), (16, 'Django-Model:VehiculeActiviteDuplicata'), (9, 'Location batiments municipaux'), (4, 'Django-Model:VisiteSiteTouristique'), (12, 'Django-Model:VehiculeActivite'), (17, 'Django-Model:VehiculeProprietaireDuplicata')], null=True),
        ),
    ]
