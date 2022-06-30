# Generated by Django 2.0.7 on 2018-10-12 13:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mod_parametrage', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notification',
            name='entity',
            field=models.IntegerField(choices=[(2, 'Django-Model:Marche'), (11, 'Django-Model:VehiculeActivite'), (16, 'Django-Model:VehiculeActiviteDuplicata'), (17, 'Django-Model:VehiculeProprietaireDuplicata'), (8, 'Django-Model:AllocationPlaceMarche'), (5, 'Django-Model:AllocationEspacePublique'), (4, 'Django-Model:VisiteSiteTouristique'), (10, 'Django-Model:FoncierParcelle'), (12, 'Django-Model:VehiculeActivite'), (6, 'Django-Model:AllocationPanneauPublicitaire'), (14, 'Django-Model:BaseActiviteDuplicata'), (7, 'Django-Model:PubliciteMurCloture'), (9, 'Location batiments municipaux'), (15, 'Django-Model:FoncierParcelleDuplicata'), (13, 'Django-Model:VehiculeProprietaire'), (18, 'Django-Model:BetailsPropriete'), (1, 'Django-Model:Standard'), (3, 'Django-Model:ActiviteExceptionnel')], null=True),
        ),
        migrations.AlterUniqueTogether(
            name='quartier',
            unique_together={('zone', 'nom', 'numero')},
        ),
        migrations.AlterIndexTogether(
            name='quartier',
            index_together={('zone', 'nom', 'numero')},
        ),
    ]
