# Generated by Django 2.0.7 on 2020-05-07 10:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mod_parametrage', '0107_auto_20200505_1652'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notification',
            name='entity',
            field=models.PositiveSmallIntegerField(choices=[(2, 'Django-Model:Marche'), (18, 'Django-Model:BetailsPropriete'), (7, 'Django-Model:PubliciteMurCloture'), (3, 'Django-Model:ActiviteExceptionnel'), (10, 'Django-Model:FoncierParcelle'), (14, 'Django-Model:BaseActiviteDuplicata'), (11, 'Django-Model:VehiculeActivite'), (17, 'Django-Model:VehiculeProprietaireDuplicata'), (16, 'Django-Model:VehiculeActiviteDuplicata'), (1, 'Django-Model:Standard'), (8, 'Django-Model:AllocationPlaceMarche'), (6, 'Django-Model:AllocationPanneauPublicitaire'), (13, 'Django-Model:VehiculeProprietaire'), (5, 'Django-Model:AllocationEspacePublique'), (4, 'Django-Model:VisiteSiteTouristique'), (12, 'Django-Model:VehiculeActivite'), (15, 'Django-Model:FoncierParcelleDuplicata'), (9, 'Location batiments municipaux')], null=True),
        ),
    ]
