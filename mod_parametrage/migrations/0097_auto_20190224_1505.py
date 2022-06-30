# Generated by Django 2.0.7 on 2019-02-24 13:05

import datetime
from decimal import Decimal
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mod_parametrage', '0096_auto_20190224_1501'),
    ]

    operations = [
        migrations.CreateModel(
            name='Penalite',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_debut', models.DateField(default=datetime.date(1900, 1, 1))),
                ('date_fin', models.DateField(default=datetime.date(1900, 1, 1))),
                ('taux', models.DecimalField(decimal_places=1, default=0.0, max_digits=10, validators=[django.core.validators.MinValueValidator(Decimal('0.0'))])),
            ],
            options={
                'ordering': ('id',),
            },
        ),
        migrations.AlterField(
            model_name='notification',
            name='entity',
            field=models.IntegerField(choices=[(14, 'Django-Model:BaseActiviteDuplicata'), (3, 'Django-Model:ActiviteExceptionnel'), (10, 'Django-Model:FoncierParcelle'), (12, 'Django-Model:VehiculeActivite'), (6, 'Django-Model:AllocationPanneauPublicitaire'), (4, 'Django-Model:VisiteSiteTouristique'), (2, 'Django-Model:Marche'), (7, 'Django-Model:PubliciteMurCloture'), (17, 'Django-Model:VehiculeProprietaireDuplicata'), (1, 'Django-Model:Standard'), (18, 'Django-Model:BetailsPropriete'), (9, 'Location batiments municipaux'), (11, 'Django-Model:VehiculeActivite'), (8, 'Django-Model:AllocationPlaceMarche'), (13, 'Django-Model:VehiculeProprietaire'), (15, 'Django-Model:FoncierParcelleDuplicata'), (16, 'Django-Model:VehiculeActiviteDuplicata'), (5, 'Django-Model:AllocationEspacePublique')], null=True),
        ),
    ]
