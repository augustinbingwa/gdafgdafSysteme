# Generated by Django 2.0.7 on 2018-11-02 07:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mod_parametrage', '0026_auto_20181101_2330'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notification',
            name='entity',
            field=models.IntegerField(choices=[(15, 'Django-Model:FoncierParcelleDuplicata'), (8, 'Django-Model:AllocationPlaceMarche'), (9, 'Location batiments municipaux'), (4, 'Django-Model:VisiteSiteTouristique'), (10, 'Django-Model:FoncierParcelle'), (13, 'Django-Model:VehiculeProprietaire'), (14, 'Django-Model:BaseActiviteDuplicata'), (12, 'Django-Model:VehiculeActivite'), (16, 'Django-Model:VehiculeActiviteDuplicata'), (17, 'Django-Model:VehiculeProprietaireDuplicata'), (18, 'Django-Model:BetailsPropriete'), (11, 'Django-Model:VehiculeActivite'), (3, 'Django-Model:ActiviteExceptionnel'), (2, 'Django-Model:Marche'), (5, 'Django-Model:AllocationEspacePublique'), (6, 'Django-Model:AllocationPanneauPublicitaire'), (1, 'Django-Model:Standard'), (7, 'Django-Model:PubliciteMurCloture')], null=True),
        ),
    ]
