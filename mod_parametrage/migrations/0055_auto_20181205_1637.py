# Generated by Django 2.0.7 on 2018-12-05 14:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mod_parametrage', '0054_auto_20181205_1626'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notification',
            name='entity',
            field=models.IntegerField(choices=[(2, 'Django-Model:Marche'), (1, 'Django-Model:Standard'), (11, 'Django-Model:VehiculeActivite'), (12, 'Django-Model:VehiculeActivite'), (14, 'Django-Model:BaseActiviteDuplicata'), (15, 'Django-Model:FoncierParcelleDuplicata'), (16, 'Django-Model:VehiculeActiviteDuplicata'), (6, 'Django-Model:AllocationPanneauPublicitaire'), (7, 'Django-Model:PubliciteMurCloture'), (9, 'Location batiments municipaux'), (10, 'Django-Model:FoncierParcelle'), (4, 'Django-Model:VisiteSiteTouristique'), (13, 'Django-Model:VehiculeProprietaire'), (17, 'Django-Model:VehiculeProprietaireDuplicata'), (18, 'Django-Model:BetailsPropriete'), (8, 'Django-Model:AllocationPlaceMarche'), (3, 'Django-Model:ActiviteExceptionnel'), (5, 'Django-Model:AllocationEspacePublique')], null=True),
        ),
    ]