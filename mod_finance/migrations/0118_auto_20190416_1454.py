# Generated by Django 2.0.7 on 2019-04-16 12:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mod_finance', '0117_auto_20190416_1449'),
    ]

    operations = [
        migrations.AlterField(
            model_name='avisimposition',
            name='entity',
            field=models.PositiveSmallIntegerField(choices=[(9, 'Location batiments municipaux'), (1, 'Django-Model:Standard'), (3, 'Django-Model:ActiviteExceptionnel'), (15, 'Django-Model:FoncierParcelleDuplicata'), (10, 'Django-Model:FoncierParcelle'), (13, 'Django-Model:VehiculeProprietaire'), (8, 'Django-Model:AllocationPlaceMarche'), (18, 'Django-Model:BetailsPropriete'), (16, 'Django-Model:VehiculeActiviteDuplicata'), (6, 'Django-Model:AllocationPanneauPublicitaire'), (17, 'Django-Model:VehiculeProprietaireDuplicata'), (11, 'Django-Model:VehiculeActivite'), (7, 'Django-Model:PubliciteMurCloture'), (5, 'Django-Model:AllocationEspacePublique'), (2, 'Django-Model:Marche'), (12, 'Django-Model:VehiculeActivite'), (4, 'Django-Model:VisiteSiteTouristique'), (14, 'Django-Model:BaseActiviteDuplicata')], null=True),
        ),
        migrations.AlterField(
            model_name='noteimposition',
            name='entity',
            field=models.PositiveSmallIntegerField(choices=[(9, 'Location batiments municipaux'), (1, 'Django-Model:Standard'), (3, 'Django-Model:ActiviteExceptionnel'), (15, 'Django-Model:FoncierParcelleDuplicata'), (10, 'Django-Model:FoncierParcelle'), (13, 'Django-Model:VehiculeProprietaire'), (8, 'Django-Model:AllocationPlaceMarche'), (18, 'Django-Model:BetailsPropriete'), (16, 'Django-Model:VehiculeActiviteDuplicata'), (6, 'Django-Model:AllocationPanneauPublicitaire'), (17, 'Django-Model:VehiculeProprietaireDuplicata'), (11, 'Django-Model:VehiculeActivite'), (7, 'Django-Model:PubliciteMurCloture'), (5, 'Django-Model:AllocationEspacePublique'), (2, 'Django-Model:Marche'), (12, 'Django-Model:VehiculeActivite'), (4, 'Django-Model:VisiteSiteTouristique'), (14, 'Django-Model:BaseActiviteDuplicata')], null=True),
        ),
        migrations.AlterField(
            model_name='periode',
            name='element',
            field=models.IntegerField(choices=[(13, '1er TRIMESTRE'), (15, '3e TRIMESTRE'), (1, 'JANVIER'), (8, 'AOUT'), (11, 'NOVEMBRE'), (18, '2e SEMESTRE'), (6, 'JUIN'), (14, '2e TRIMESTRE'), (16, '4e TRIMESTRE'), (7, 'JUILLET'), (19, 'ANNEE'), (12, 'DECEMBRE'), (17, '1er SEMESTRE'), (9, 'SEPTEMBRE'), (5, 'MAI'), (10, 'OCTOBRE'), (2, 'FEVRIER'), (4, 'AVRIL'), (3, 'MARS')], verbose_name='Elements de période'),
        ),
        migrations.AlterField(
            model_name='periodetype',
            name='categorie',
            field=models.IntegerField(choices=[(0, 'Autre'), (1, 'Mensuelle'), (3, 'Semestrielle'), (4, 'Annuelle'), (2, 'Trimestrielle')], default=0, verbose_name='catégorie de périodes'),
        ),
    ]
