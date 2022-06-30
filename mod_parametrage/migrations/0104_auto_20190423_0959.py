# Generated by Django 2.0.7 on 2019-04-23 07:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mod_parametrage', '0103_auto_20190416_1449'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notification',
            name='entity',
            field=models.PositiveSmallIntegerField(choices=[(13, 'Django-Model:VehiculeProprietaire'), (11, 'Django-Model:VehiculeActivite'), (6, 'Django-Model:AllocationPanneauPublicitaire'), (5, 'Django-Model:AllocationEspacePublique'), (17, 'Django-Model:VehiculeProprietaireDuplicata'), (9, 'Location batiments municipaux'), (7, 'Django-Model:PubliciteMurCloture'), (3, 'Django-Model:ActiviteExceptionnel'), (4, 'Django-Model:VisiteSiteTouristique'), (10, 'Django-Model:FoncierParcelle'), (18, 'Django-Model:BetailsPropriete'), (1, 'Django-Model:Standard'), (12, 'Django-Model:VehiculeActivite'), (2, 'Django-Model:Marche'), (15, 'Django-Model:FoncierParcelleDuplicata'), (16, 'Django-Model:VehiculeActiviteDuplicata'), (8, 'Django-Model:AllocationPlaceMarche'), (14, 'Django-Model:BaseActiviteDuplicata')], null=True),
        ),
        migrations.AlterField(
            model_name='notification',
            name='entity_id',
            field=models.IntegerField(null=True),
        ),
    ]