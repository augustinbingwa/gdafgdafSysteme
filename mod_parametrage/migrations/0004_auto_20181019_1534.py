# Generated by Django 2.0.7 on 2018-10-19 13:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mod_parametrage', '0003_auto_20181019_1238'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notification',
            name='entity',
            field=models.IntegerField(choices=[(2, 'Django-Model:Marche'), (6, 'Django-Model:AllocationPanneauPublicitaire'), (5, 'Django-Model:AllocationEspacePublique'), (14, 'Django-Model:BaseActiviteDuplicata'), (17, 'Django-Model:VehiculeProprietaireDuplicata'), (12, 'Django-Model:VehiculeActivite'), (13, 'Django-Model:VehiculeProprietaire'), (3, 'Django-Model:ActiviteExceptionnel'), (9, 'Location batiments municipaux'), (15, 'Django-Model:FoncierParcelleDuplicata'), (16, 'Django-Model:VehiculeActiviteDuplicata'), (1, 'Django-Model:Standard'), (4, 'Django-Model:VisiteSiteTouristique'), (7, 'Django-Model:PubliciteMurCloture'), (8, 'Django-Model:AllocationPlaceMarche'), (11, 'Django-Model:VehiculeActivite'), (18, 'Django-Model:BetailsPropriete'), (10, 'Django-Model:FoncierParcelle')], null=True),
        ),
    ]