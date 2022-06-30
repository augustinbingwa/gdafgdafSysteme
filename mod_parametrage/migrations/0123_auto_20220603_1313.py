# Generated by Django 2.2.28 on 2022-06-03 11:13

import datetime
from decimal import Decimal
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mod_parametrage', '0122_auto_20220210_1616'),
    ]

    operations = [
        migrations.CreateModel(
            name='PenaliteTransport',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('entity', models.IntegerField(default=11)),
                ('date_debut', models.DateField(default=datetime.date(1900, 1, 1))),
                ('date_fin', models.DateField(default=datetime.date(1900, 1, 1))),
                ('taux_ou_montant', models.DecimalField(decimal_places=1, default=0.0, max_digits=10, validators=[django.core.validators.MinValueValidator(Decimal('0.0'))])),
                ('is_taux_date_ecoule', models.BooleanField(default=False)),
            ],
            options={
                'ordering': ('id',),
            },
        ),
        migrations.AlterField(
            model_name='notification',
            name='entity',
            field=models.PositiveSmallIntegerField(choices=[(2, 'Django-Model:Marche'), (11, 'Django-Model:VehiculeActivite'), (3, 'Django-Model:ActiviteExceptionnel'), (8, 'Django-Model:AllocationPlaceMarche'), (12, 'Django-Model:VehiculeActivite'), (13, 'Django-Model:VehiculeProprietaire'), (17, 'Django-Model:VehiculeProprietaireDuplicata'), (9, 'Location batiments municipaux'), (16, 'Django-Model:VehiculeActiviteDuplicata'), (18, 'Django-Model:BetailsPropriete'), (4, 'Django-Model:VisiteSiteTouristique'), (7, 'Django-Model:PubliciteMurCloture'), (10, 'Django-Model:FoncierParcelle'), (5, 'Django-Model:AllocationEspacePublique'), (14, 'Django-Model:BaseActiviteDuplicata'), (15, 'Django-Model:FoncierParcelleDuplicata'), (1, 'Django-Model:Standard'), (6, 'Django-Model:AllocationPanneauPublicitaire')], null=True),
        ),
    ]