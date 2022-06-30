# Generated by Django 2.0.7 on 2019-01-10 20:10

from decimal import Decimal
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mod_finance', '0081_auto_20190110_2129'),
    ]

    operations = [
        migrations.AlterField(
            model_name='avisimposition',
            name='entity',
            field=models.IntegerField(choices=[(12, 'Django-Model:VehiculeActivite'), (4, 'Django-Model:VisiteSiteTouristique'), (9, 'Location batiments municipaux'), (2, 'Django-Model:Marche'), (15, 'Django-Model:FoncierParcelleDuplicata'), (3, 'Django-Model:ActiviteExceptionnel'), (5, 'Django-Model:AllocationEspacePublique'), (11, 'Django-Model:VehiculeActivite'), (16, 'Django-Model:VehiculeActiviteDuplicata'), (6, 'Django-Model:AllocationPanneauPublicitaire'), (17, 'Django-Model:VehiculeProprietaireDuplicata'), (18, 'Django-Model:BetailsPropriete'), (1, 'Django-Model:Standard'), (13, 'Django-Model:VehiculeProprietaire'), (7, 'Django-Model:PubliciteMurCloture'), (10, 'Django-Model:FoncierParcelle'), (8, 'Django-Model:AllocationPlaceMarche'), (14, 'Django-Model:BaseActiviteDuplicata')], null=True),
        ),
        migrations.AlterField(
            model_name='avisimposition',
            name='montant_total',
            field=models.DecimalField(decimal_places=0, max_digits=10, validators=[django.core.validators.MinValueValidator(Decimal('0'))]),
        ),
        migrations.AlterField(
            model_name='avisimposition',
            name='taxe_montant',
            field=models.DecimalField(decimal_places=0, max_digits=10, validators=[django.core.validators.MinValueValidator(Decimal('0'))]),
        ),
        migrations.AlterField(
            model_name='noteimposition',
            name='entity',
            field=models.IntegerField(choices=[(12, 'Django-Model:VehiculeActivite'), (4, 'Django-Model:VisiteSiteTouristique'), (9, 'Location batiments municipaux'), (2, 'Django-Model:Marche'), (15, 'Django-Model:FoncierParcelleDuplicata'), (3, 'Django-Model:ActiviteExceptionnel'), (5, 'Django-Model:AllocationEspacePublique'), (11, 'Django-Model:VehiculeActivite'), (16, 'Django-Model:VehiculeActiviteDuplicata'), (6, 'Django-Model:AllocationPanneauPublicitaire'), (17, 'Django-Model:VehiculeProprietaireDuplicata'), (18, 'Django-Model:BetailsPropriete'), (1, 'Django-Model:Standard'), (13, 'Django-Model:VehiculeProprietaire'), (7, 'Django-Model:PubliciteMurCloture'), (10, 'Django-Model:FoncierParcelle'), (8, 'Django-Model:AllocationPlaceMarche'), (14, 'Django-Model:BaseActiviteDuplicata')], null=True),
        ),
        migrations.AlterField(
            model_name='noteimposition',
            name='taxe_montant',
            field=models.DecimalField(decimal_places=0, max_digits=10, validators=[django.core.validators.MinValueValidator(Decimal('0'))]),
        ),
        migrations.AlterField(
            model_name='noteimposition',
            name='taxe_montant_paye',
            field=models.DecimalField(decimal_places=0, default=0.0, max_digits=10, validators=[django.core.validators.MinValueValidator(Decimal('0'))]),
        ),
        migrations.AlterField(
            model_name='noteimpositionpaiement',
            name='montant_tranche',
            field=models.DecimalField(decimal_places=0, max_digits=10, validators=[django.core.validators.MinValueValidator(Decimal('0'))]),
        ),
        migrations.AlterField(
            model_name='periode',
            name='element',
            field=models.IntegerField(choices=[(11, 'Novembre'), (15, '3e Trimestre'), (4, 'Avril'), (2, 'Février'), (16, '4e Trimestre'), (17, '1er Semestre'), (7, 'Juillet'), (10, 'Octobre'), (13, '1er Trimestre'), (14, '2e Trimestre'), (5, 'Mai'), (3, 'Mars'), (18, '2e Semestre'), (19, 'Année'), (8, 'Août'), (1, 'Janvier'), (6, 'Juin'), (9, 'Septembre'), (12, 'Décembre')], verbose_name='Elements de période'),
        ),
        migrations.AlterField(
            model_name='periodetype',
            name='categorie',
            field=models.IntegerField(choices=[(1, 'Mensuelle'), (4, 'Annuelle'), (3, 'Semestrielle'), (0, 'Autre'), (2, 'Trimestrielle')], default=0, verbose_name='catégorie de périodes'),
        ),
    ]
