# Generated by Django 3.1.7 on 2022-06-14 09:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mod_finance', '0137_auto_20220603_1313'),
    ]

    operations = [
        migrations.AlterField(
            model_name='avisimposition',
            name='entity',
            field=models.PositiveSmallIntegerField(choices=[(7, 'Django-Model:PubliciteMurCloture'), (17, 'Django-Model:VehiculeProprietaireDuplicata'), (8, 'Django-Model:AllocationPlaceMarche'), (14, 'Django-Model:BaseActiviteDuplicata'), (2, 'Django-Model:Marche'), (9, 'Location batiments municipaux'), (16, 'Django-Model:VehiculeActiviteDuplicata'), (10, 'Django-Model:FoncierParcelle'), (15, 'Django-Model:FoncierParcelleDuplicata'), (6, 'Django-Model:AllocationPanneauPublicitaire'), (4, 'Django-Model:VisiteSiteTouristique'), (18, 'Django-Model:BetailsPropriete'), (3, 'Django-Model:ActiviteExceptionnel'), (11, 'Django-Model:VehiculeActivite'), (1, 'Django-Model:Standard'), (12, 'Django-Model:VehiculeActivite'), (13, 'Django-Model:VehiculeProprietaire'), (5, 'Django-Model:AllocationEspacePublique')], null=True),
        ),
        migrations.AlterField(
            model_name='noteimposition',
            name='entity',
            field=models.PositiveSmallIntegerField(choices=[(7, 'Django-Model:PubliciteMurCloture'), (17, 'Django-Model:VehiculeProprietaireDuplicata'), (8, 'Django-Model:AllocationPlaceMarche'), (14, 'Django-Model:BaseActiviteDuplicata'), (2, 'Django-Model:Marche'), (9, 'Location batiments municipaux'), (16, 'Django-Model:VehiculeActiviteDuplicata'), (10, 'Django-Model:FoncierParcelle'), (15, 'Django-Model:FoncierParcelleDuplicata'), (6, 'Django-Model:AllocationPanneauPublicitaire'), (4, 'Django-Model:VisiteSiteTouristique'), (18, 'Django-Model:BetailsPropriete'), (3, 'Django-Model:ActiviteExceptionnel'), (11, 'Django-Model:VehiculeActivite'), (1, 'Django-Model:Standard'), (12, 'Django-Model:VehiculeActivite'), (13, 'Django-Model:VehiculeProprietaire'), (5, 'Django-Model:AllocationEspacePublique')], null=True),
        ),
        migrations.AlterField(
            model_name='noteimpositiondelete',
            name='entity',
            field=models.PositiveSmallIntegerField(choices=[(7, 'Django-Model:PubliciteMurCloture'), (17, 'Django-Model:VehiculeProprietaireDuplicata'), (8, 'Django-Model:AllocationPlaceMarche'), (14, 'Django-Model:BaseActiviteDuplicata'), (2, 'Django-Model:Marche'), (9, 'Location batiments municipaux'), (16, 'Django-Model:VehiculeActiviteDuplicata'), (10, 'Django-Model:FoncierParcelle'), (15, 'Django-Model:FoncierParcelleDuplicata'), (6, 'Django-Model:AllocationPanneauPublicitaire'), (4, 'Django-Model:VisiteSiteTouristique'), (18, 'Django-Model:BetailsPropriete'), (3, 'Django-Model:ActiviteExceptionnel'), (11, 'Django-Model:VehiculeActivite'), (1, 'Django-Model:Standard'), (12, 'Django-Model:VehiculeActivite'), (13, 'Django-Model:VehiculeProprietaire'), (5, 'Django-Model:AllocationEspacePublique')], null=True),
        ),
        migrations.AlterField(
            model_name='periode',
            name='element',
            field=models.IntegerField(choices=[(17, '1er SEMESTRE'), (4, 'AVRIL'), (14, '2e TRIMESTRE'), (13, '1er TRIMESTRE'), (6, 'JUIN'), (16, '4e TRIMESTRE'), (18, '2e SEMESTRE'), (1, 'JANVIER'), (9, 'SEPTEMBRE'), (5, 'MAI'), (3, 'MARS'), (15, '3e TRIMESTRE'), (2, 'FEVRIER'), (10, 'OCTOBRE'), (8, 'AOUT'), (19, 'ANNEE'), (7, 'JUILLET'), (12, 'DECEMBRE'), (11, 'NOVEMBRE')], verbose_name='Elements de période'),
        ),
        migrations.AlterField(
            model_name='periodetype',
            name='categorie',
            field=models.IntegerField(choices=[(0, 'Autre'), (1, 'Mensuelle'), (3, 'Semestrielle'), (2, 'Trimestrielle'), (4, 'Annuelle')], default=0, verbose_name='catégorie de périodes'),
        ),
    ]