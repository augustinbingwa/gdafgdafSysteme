# Generated by Django 2.0.7 on 2019-01-04 02:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mod_parametrage', '0068_auto_20190104_0405'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notification',
            name='entity',
            field=models.IntegerField(choices=[(13, 'Django-Model:VehiculeProprietaire'), (1, 'Django-Model:Standard'), (7, 'Django-Model:PubliciteMurCloture'), (6, 'Django-Model:AllocationPanneauPublicitaire'), (9, 'Location batiments municipaux'), (10, 'Django-Model:FoncierParcelle'), (15, 'Django-Model:FoncierParcelleDuplicata'), (16, 'Django-Model:VehiculeActiviteDuplicata'), (2, 'Django-Model:Marche'), (12, 'Django-Model:VehiculeActivite'), (11, 'Django-Model:VehiculeActivite'), (14, 'Django-Model:BaseActiviteDuplicata'), (17, 'Django-Model:VehiculeProprietaireDuplicata'), (3, 'Django-Model:ActiviteExceptionnel'), (18, 'Django-Model:BetailsPropriete'), (5, 'Django-Model:AllocationEspacePublique'), (4, 'Django-Model:VisiteSiteTouristique'), (8, 'Django-Model:AllocationPlaceMarche')], null=True),
        ),
    ]
