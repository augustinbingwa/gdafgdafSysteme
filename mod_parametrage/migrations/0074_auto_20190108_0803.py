# Generated by Django 2.0.7 on 2019-01-08 06:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mod_parametrage', '0073_auto_20190107_2340'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notification',
            name='entity',
            field=models.IntegerField(choices=[(1, 'Django-Model:Standard'), (15, 'Django-Model:FoncierParcelleDuplicata'), (12, 'Django-Model:VehiculeActivite'), (10, 'Django-Model:FoncierParcelle'), (17, 'Django-Model:VehiculeProprietaireDuplicata'), (5, 'Django-Model:AllocationEspacePublique'), (3, 'Django-Model:ActiviteExceptionnel'), (9, 'Location batiments municipaux'), (6, 'Django-Model:AllocationPanneauPublicitaire'), (16, 'Django-Model:VehiculeActiviteDuplicata'), (7, 'Django-Model:PubliciteMurCloture'), (4, 'Django-Model:VisiteSiteTouristique'), (11, 'Django-Model:VehiculeActivite'), (8, 'Django-Model:AllocationPlaceMarche'), (13, 'Django-Model:VehiculeProprietaire'), (14, 'Django-Model:BaseActiviteDuplicata'), (2, 'Django-Model:Marche'), (18, 'Django-Model:BetailsPropriete')], null=True),
        ),
    ]