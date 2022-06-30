# Generated by Django 2.0.7 on 2019-01-04 08:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mod_parametrage', '0069_auto_20190104_0408'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notification',
            name='entity',
            field=models.IntegerField(choices=[(9, 'Location batiments municipaux'), (2, 'Django-Model:Marche'), (12, 'Django-Model:VehiculeActivite'), (13, 'Django-Model:VehiculeProprietaire'), (14, 'Django-Model:BaseActiviteDuplicata'), (8, 'Django-Model:AllocationPlaceMarche'), (5, 'Django-Model:AllocationEspacePublique'), (1, 'Django-Model:Standard'), (6, 'Django-Model:AllocationPanneauPublicitaire'), (3, 'Django-Model:ActiviteExceptionnel'), (17, 'Django-Model:VehiculeProprietaireDuplicata'), (7, 'Django-Model:PubliciteMurCloture'), (4, 'Django-Model:VisiteSiteTouristique'), (10, 'Django-Model:FoncierParcelle'), (11, 'Django-Model:VehiculeActivite'), (15, 'Django-Model:FoncierParcelleDuplicata'), (16, 'Django-Model:VehiculeActiviteDuplicata'), (18, 'Django-Model:BetailsPropriete')], null=True),
        ),
    ]