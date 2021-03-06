# Generated by Django 2.0.7 on 2018-11-20 09:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mod_parametrage', '0046_auto_20181119_1118'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notification',
            name='entity',
            field=models.IntegerField(choices=[(17, 'Django-Model:VehiculeProprietaireDuplicata'), (9, 'Location batiments municipaux'), (4, 'Django-Model:VisiteSiteTouristique'), (11, 'Django-Model:VehiculeActivite'), (14, 'Django-Model:BaseActiviteDuplicata'), (10, 'Django-Model:FoncierParcelle'), (8, 'Django-Model:AllocationPlaceMarche'), (7, 'Django-Model:PubliciteMurCloture'), (16, 'Django-Model:VehiculeActiviteDuplicata'), (1, 'Django-Model:Standard'), (18, 'Django-Model:BetailsPropriete'), (12, 'Django-Model:VehiculeActivite'), (15, 'Django-Model:FoncierParcelleDuplicata'), (5, 'Django-Model:AllocationEspacePublique'), (6, 'Django-Model:AllocationPanneauPublicitaire'), (2, 'Django-Model:Marche'), (3, 'Django-Model:ActiviteExceptionnel'), (13, 'Django-Model:VehiculeProprietaire')], null=True),
        ),
    ]
