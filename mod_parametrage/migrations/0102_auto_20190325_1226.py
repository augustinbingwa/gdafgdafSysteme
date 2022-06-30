# Generated by Django 2.0.7 on 2019-03-25 10:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mod_parametrage', '0101_auto_20190325_1143'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notification',
            name='entity',
            field=models.IntegerField(choices=[(16, 'Django-Model:VehiculeActiviteDuplicata'), (10, 'Django-Model:FoncierParcelle'), (9, 'Location batiments municipaux'), (17, 'Django-Model:VehiculeProprietaireDuplicata'), (11, 'Django-Model:VehiculeActivite'), (14, 'Django-Model:BaseActiviteDuplicata'), (15, 'Django-Model:FoncierParcelleDuplicata'), (5, 'Django-Model:AllocationEspacePublique'), (7, 'Django-Model:PubliciteMurCloture'), (2, 'Django-Model:Marche'), (12, 'Django-Model:VehiculeActivite'), (4, 'Django-Model:VisiteSiteTouristique'), (1, 'Django-Model:Standard'), (3, 'Django-Model:ActiviteExceptionnel'), (8, 'Django-Model:AllocationPlaceMarche'), (13, 'Django-Model:VehiculeProprietaire'), (6, 'Django-Model:AllocationPanneauPublicitaire'), (18, 'Django-Model:BetailsPropriete')], null=True),
        ),
    ]
