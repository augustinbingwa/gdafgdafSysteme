# Generated by Django 2.0.7 on 2018-11-06 09:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mod_parametrage', '0035_auto_20181106_0951'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notification',
            name='entity',
            field=models.IntegerField(choices=[(13, 'Django-Model:VehiculeProprietaire'), (11, 'Django-Model:VehiculeActivite'), (17, 'Django-Model:VehiculeProprietaireDuplicata'), (2, 'Django-Model:Marche'), (14, 'Django-Model:BaseActiviteDuplicata'), (18, 'Django-Model:BetailsPropriete'), (3, 'Django-Model:ActiviteExceptionnel'), (5, 'Django-Model:AllocationEspacePublique'), (9, 'Location batiments municipaux'), (12, 'Django-Model:VehiculeActivite'), (15, 'Django-Model:FoncierParcelleDuplicata'), (8, 'Django-Model:AllocationPlaceMarche'), (10, 'Django-Model:FoncierParcelle'), (4, 'Django-Model:VisiteSiteTouristique'), (1, 'Django-Model:Standard'), (7, 'Django-Model:PubliciteMurCloture'), (16, 'Django-Model:VehiculeActiviteDuplicata'), (6, 'Django-Model:AllocationPanneauPublicitaire')], null=True),
        ),
    ]
