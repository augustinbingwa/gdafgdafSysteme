# Generated by Django 2.0.7 on 2018-11-26 19:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mod_parametrage', '0050_auto_20181121_1326'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notification',
            name='entity',
            field=models.IntegerField(choices=[(8, 'Django-Model:AllocationPlaceMarche'), (6, 'Django-Model:AllocationPanneauPublicitaire'), (4, 'Django-Model:VisiteSiteTouristique'), (1, 'Django-Model:Standard'), (10, 'Django-Model:FoncierParcelle'), (2, 'Django-Model:Marche'), (5, 'Django-Model:AllocationEspacePublique'), (13, 'Django-Model:VehiculeProprietaire'), (3, 'Django-Model:ActiviteExceptionnel'), (17, 'Django-Model:VehiculeProprietaireDuplicata'), (12, 'Django-Model:VehiculeActivite'), (15, 'Django-Model:FoncierParcelleDuplicata'), (7, 'Django-Model:PubliciteMurCloture'), (9, 'Location batiments municipaux'), (14, 'Django-Model:BaseActiviteDuplicata'), (16, 'Django-Model:VehiculeActiviteDuplicata'), (18, 'Django-Model:BetailsPropriete'), (11, 'Django-Model:VehiculeActivite')], null=True),
        ),
    ]
