# Generated by Django 2.0.7 on 2019-01-17 07:13

from decimal import Decimal
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mod_finance', '0093_auto_20190112_1127'),
    ]

    operations = [
        migrations.AddField(
            model_name='noteimpositionpaiement',
            name='montant_excedant',
            field=models.DecimalField(decimal_places=0, default=0, max_digits=10, validators=[django.core.validators.MinValueValidator(Decimal('0'))]),
        ),
        migrations.AlterField(
            model_name='avisimposition',
            name='entity',
            field=models.IntegerField(choices=[(15, 'Django-Model:FoncierParcelleDuplicata'), (14, 'Django-Model:BaseActiviteDuplicata'), (12, 'Django-Model:VehiculeActivite'), (17, 'Django-Model:VehiculeProprietaireDuplicata'), (10, 'Django-Model:FoncierParcelle'), (9, 'Location batiments municipaux'), (18, 'Django-Model:BetailsPropriete'), (5, 'Django-Model:AllocationEspacePublique'), (4, 'Django-Model:VisiteSiteTouristique'), (8, 'Django-Model:AllocationPlaceMarche'), (16, 'Django-Model:VehiculeActiviteDuplicata'), (7, 'Django-Model:PubliciteMurCloture'), (11, 'Django-Model:VehiculeActivite'), (1, 'Django-Model:Standard'), (13, 'Django-Model:VehiculeProprietaire'), (2, 'Django-Model:Marche'), (6, 'Django-Model:AllocationPanneauPublicitaire'), (3, 'Django-Model:ActiviteExceptionnel')], null=True),
        ),
        migrations.AlterField(
            model_name='noteimposition',
            name='entity',
            field=models.IntegerField(choices=[(15, 'Django-Model:FoncierParcelleDuplicata'), (14, 'Django-Model:BaseActiviteDuplicata'), (12, 'Django-Model:VehiculeActivite'), (17, 'Django-Model:VehiculeProprietaireDuplicata'), (10, 'Django-Model:FoncierParcelle'), (9, 'Location batiments municipaux'), (18, 'Django-Model:BetailsPropriete'), (5, 'Django-Model:AllocationEspacePublique'), (4, 'Django-Model:VisiteSiteTouristique'), (8, 'Django-Model:AllocationPlaceMarche'), (16, 'Django-Model:VehiculeActiviteDuplicata'), (7, 'Django-Model:PubliciteMurCloture'), (11, 'Django-Model:VehiculeActivite'), (1, 'Django-Model:Standard'), (13, 'Django-Model:VehiculeProprietaire'), (2, 'Django-Model:Marche'), (6, 'Django-Model:AllocationPanneauPublicitaire'), (3, 'Django-Model:ActiviteExceptionnel')], null=True),
        ),
        migrations.AlterField(
            model_name='periode',
            name='element',
            field=models.IntegerField(choices=[(16, '4e Trimestre'), (7, 'Juillet'), (18, '2e Semestre'), (15, '3e Trimestre'), (2, 'Février'), (5, 'Mai'), (3, 'Mars'), (13, '1er Trimestre'), (6, 'Juin'), (1, 'Janvier'), (11, 'Novembre'), (8, 'Août'), (14, '2e Trimestre'), (10, 'Octobre'), (9, 'Septembre'), (4, 'Avril'), (19, 'Année'), (17, '1er Semestre'), (12, 'Décembre')], verbose_name='Elements de période'),
        ),
        migrations.AlterField(
            model_name='periodetype',
            name='categorie',
            field=models.IntegerField(choices=[(0, 'Autre'), (3, 'Semestrielle'), (4, 'Annuelle'), (2, 'Trimestrielle'), (1, 'Mensuelle')], default=0, verbose_name='catégorie de périodes'),
        ),
    ]
