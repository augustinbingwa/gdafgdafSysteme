# Generated by Django 2.0.7 on 2018-11-06 09:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mod_parametrage', '0037_auto_20181106_1143'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notification',
            name='entity',
            field=models.IntegerField(choices=[(13, 'Django-Model:VehiculeProprietaire'), (5, 'Django-Model:AllocationEspacePublique'), (10, 'Django-Model:FoncierParcelle'), (14, 'Django-Model:BaseActiviteDuplicata'), (2, 'Django-Model:Marche'), (1, 'Django-Model:Standard'), (17, 'Django-Model:VehiculeProprietaireDuplicata'), (7, 'Django-Model:PubliciteMurCloture'), (4, 'Django-Model:VisiteSiteTouristique'), (12, 'Django-Model:VehiculeActivite'), (15, 'Django-Model:FoncierParcelleDuplicata'), (16, 'Django-Model:VehiculeActiviteDuplicata'), (18, 'Django-Model:BetailsPropriete'), (8, 'Django-Model:AllocationPlaceMarche'), (6, 'Django-Model:AllocationPanneauPublicitaire'), (9, 'Location batiments municipaux'), (3, 'Django-Model:ActiviteExceptionnel'), (11, 'Django-Model:VehiculeActivite')], null=True),
        ),
    ]
