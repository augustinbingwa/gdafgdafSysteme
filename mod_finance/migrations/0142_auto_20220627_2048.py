# Generated by Django 3.1.7 on 2022-06-27 18:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mod_finance', '0141_auto_20220627_2000'),
    ]

    operations = [
        migrations.AlterField(
            model_name='avisimposition',
            name='entity',
            field=models.PositiveSmallIntegerField(choices=[(20, 'Django-Model:Acte'), (5, 'Django-Model:AllocationEspacePublique'), (8, 'Django-Model:AllocationPlaceMarche'), (10, 'Django-Model:FoncierParcelle'), (6, 'Django-Model:AllocationPanneauPublicitaire'), (16, 'Django-Model:VehiculeActiviteDuplicata'), (13, 'Django-Model:VehiculeProprietaire'), (11, 'Django-Model:VehiculeActivite'), (4, 'Django-Model:VisiteSiteTouristique'), (15, 'Django-Model:FoncierParcelleDuplicata'), (7, 'Django-Model:PubliciteMurCloture'), (1, 'Django-Model:Standard'), (9, 'Django-Model:Location batiments municipaux'), (18, 'Django-Model:BetailsPropriete'), (3, 'Django-Model:ActiviteExceptionnel'), (14, 'Django-Model:BaseActiviteDuplicata'), (12, 'Django-Model:VehiculeActivite'), (19, 'Django-Model:Attestation'), (17, 'Django-Model:VehiculeProprietaireDuplicata'), (2, 'Django-Model:Marche')], null=True),
        ),
        migrations.AlterField(
            model_name='noteimposition',
            name='entity',
            field=models.PositiveSmallIntegerField(choices=[(20, 'Django-Model:Acte'), (5, 'Django-Model:AllocationEspacePublique'), (8, 'Django-Model:AllocationPlaceMarche'), (10, 'Django-Model:FoncierParcelle'), (6, 'Django-Model:AllocationPanneauPublicitaire'), (16, 'Django-Model:VehiculeActiviteDuplicata'), (13, 'Django-Model:VehiculeProprietaire'), (11, 'Django-Model:VehiculeActivite'), (4, 'Django-Model:VisiteSiteTouristique'), (15, 'Django-Model:FoncierParcelleDuplicata'), (7, 'Django-Model:PubliciteMurCloture'), (1, 'Django-Model:Standard'), (9, 'Django-Model:Location batiments municipaux'), (18, 'Django-Model:BetailsPropriete'), (3, 'Django-Model:ActiviteExceptionnel'), (14, 'Django-Model:BaseActiviteDuplicata'), (12, 'Django-Model:VehiculeActivite'), (19, 'Django-Model:Attestation'), (17, 'Django-Model:VehiculeProprietaireDuplicata'), (2, 'Django-Model:Marche')], null=True),
        ),
        migrations.AlterField(
            model_name='noteimpositiondelete',
            name='entity',
            field=models.PositiveSmallIntegerField(choices=[(20, 'Django-Model:Acte'), (5, 'Django-Model:AllocationEspacePublique'), (8, 'Django-Model:AllocationPlaceMarche'), (10, 'Django-Model:FoncierParcelle'), (6, 'Django-Model:AllocationPanneauPublicitaire'), (16, 'Django-Model:VehiculeActiviteDuplicata'), (13, 'Django-Model:VehiculeProprietaire'), (11, 'Django-Model:VehiculeActivite'), (4, 'Django-Model:VisiteSiteTouristique'), (15, 'Django-Model:FoncierParcelleDuplicata'), (7, 'Django-Model:PubliciteMurCloture'), (1, 'Django-Model:Standard'), (9, 'Django-Model:Location batiments municipaux'), (18, 'Django-Model:BetailsPropriete'), (3, 'Django-Model:ActiviteExceptionnel'), (14, 'Django-Model:BaseActiviteDuplicata'), (12, 'Django-Model:VehiculeActivite'), (19, 'Django-Model:Attestation'), (17, 'Django-Model:VehiculeProprietaireDuplicata'), (2, 'Django-Model:Marche')], null=True),
        ),
        migrations.AlterField(
            model_name='periode',
            name='element',
            field=models.IntegerField(choices=[(16, '4e TRIMESTRE'), (17, '1er SEMESTRE'), (11, 'NOVEMBRE'), (13, '1er TRIMESTRE'), (14, '2e TRIMESTRE'), (1, 'JANVIER'), (19, 'ANNEE'), (5, 'MAI'), (8, 'AOUT'), (7, 'JUILLET'), (15, '3e TRIMESTRE'), (2, 'FEVRIER'), (18, '2e SEMESTRE'), (3, 'MARS'), (9, 'SEPTEMBRE'), (6, 'JUIN'), (4, 'AVRIL'), (12, 'DECEMBRE'), (10, 'OCTOBRE')], verbose_name='Elements de p??riode'),
        ),
        migrations.AlterField(
            model_name='periodetype',
            name='categorie',
            field=models.IntegerField(choices=[(0, 'Autre'), (2, 'Trimestrielle'), (1, 'Mensuelle'), (4, 'Annuelle'), (3, 'Semestrielle')], default=0, verbose_name='cat??gorie de p??riodes'),
        ),
    ]
