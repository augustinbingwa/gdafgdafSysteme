# Generated by Django 2.0.7 on 2018-11-15 12:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mod_parametrage', '0042_auto_20181113_1651'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notification',
            name='entity',
            field=models.IntegerField(choices=[(13, 'Django-Model:VehiculeProprietaire'), (15, 'Django-Model:FoncierParcelleDuplicata'), (1, 'Django-Model:Standard'), (12, 'Django-Model:VehiculeActivite'), (9, 'Location batiments municipaux'), (16, 'Django-Model:VehiculeActiviteDuplicata'), (6, 'Django-Model:AllocationPanneauPublicitaire'), (14, 'Django-Model:BaseActiviteDuplicata'), (17, 'Django-Model:VehiculeProprietaireDuplicata'), (8, 'Django-Model:AllocationPlaceMarche'), (10, 'Django-Model:FoncierParcelle'), (18, 'Django-Model:BetailsPropriete'), (2, 'Django-Model:Marche'), (3, 'Django-Model:ActiviteExceptionnel'), (5, 'Django-Model:AllocationEspacePublique'), (4, 'Django-Model:VisiteSiteTouristique'), (7, 'Django-Model:PubliciteMurCloture'), (11, 'Django-Model:VehiculeActivite')], null=True),
        ),
    ]
