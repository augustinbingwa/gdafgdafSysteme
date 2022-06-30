# Generated by Django 2.0.7 on 2019-01-25 10:44

import datetime
from decimal import Decimal
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mod_parametrage', '0083_auto_20190125_1241'),
    ]

    operations = [
        migrations.CreateModel(
            name='Accroissement',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_debut', models.DateField(default=datetime.date(1900, 1, 1))),
                ('date_fin', models.DateField(default=datetime.date(1900, 1, 1))),
                ('taux', models.DecimalField(decimal_places=1, default=0.0, max_digits=10, validators=[django.core.validators.MinValueValidator(Decimal('0.0'))])),
                ('is_taux_annee_ecoulee', models.BooleanField(default=False)),
            ],
            options={
                'ordering': ('id',),
            },
        ),
        migrations.AlterField(
            model_name='notification',
            name='entity',
            field=models.IntegerField(choices=[(4, 'Django-Model:VisiteSiteTouristique'), (8, 'Django-Model:AllocationPlaceMarche'), (5, 'Django-Model:AllocationEspacePublique'), (10, 'Django-Model:FoncierParcelle'), (7, 'Django-Model:PubliciteMurCloture'), (17, 'Django-Model:VehiculeProprietaireDuplicata'), (11, 'Django-Model:VehiculeActivite'), (16, 'Django-Model:VehiculeActiviteDuplicata'), (14, 'Django-Model:BaseActiviteDuplicata'), (6, 'Django-Model:AllocationPanneauPublicitaire'), (2, 'Django-Model:Marche'), (13, 'Django-Model:VehiculeProprietaire'), (15, 'Django-Model:FoncierParcelleDuplicata'), (18, 'Django-Model:BetailsPropriete'), (1, 'Django-Model:Standard'), (3, 'Django-Model:ActiviteExceptionnel'), (9, 'Location batiments municipaux'), (12, 'Django-Model:VehiculeActivite')], null=True),
        ),
    ]
