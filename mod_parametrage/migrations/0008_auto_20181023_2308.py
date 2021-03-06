# Generated by Django 2.0.7 on 2018-10-23 21:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mod_parametrage', '0007_auto_20181023_2256'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notification',
            name='entity',
            field=models.IntegerField(choices=[(10, 'Django-Model:FoncierParcelle'), (15, 'Django-Model:FoncierParcelleDuplicata'), (4, 'Django-Model:VisiteSiteTouristique'), (7, 'Django-Model:PubliciteMurCloture'), (18, 'Django-Model:BetailsPropriete'), (14, 'Django-Model:BaseActiviteDuplicata'), (13, 'Django-Model:VehiculeProprietaire'), (11, 'Django-Model:VehiculeActivite'), (9, 'Location batiments municipaux'), (1, 'Django-Model:Standard'), (8, 'Django-Model:AllocationPlaceMarche'), (6, 'Django-Model:AllocationPanneauPublicitaire'), (16, 'Django-Model:VehiculeActiviteDuplicata'), (17, 'Django-Model:VehiculeProprietaireDuplicata'), (5, 'Django-Model:AllocationEspacePublique'), (2, 'Django-Model:Marche'), (3, 'Django-Model:ActiviteExceptionnel'), (12, 'Django-Model:VehiculeActivite')], null=True),
        ),
    ]
