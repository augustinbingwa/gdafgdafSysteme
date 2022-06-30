# Generated by Django 3.1.7 on 2022-02-13 06:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("mod_finance", "0135_auto_20220209_1604"),
    ]

    operations = [
        migrations.RenameField(
            model_name="noteimposition",
            old_name="taux_penalite",
            new_name="montant_restant",
        ),
        migrations.AlterField(
            model_name="avisimposition",
            name="entity",
            field=models.PositiveSmallIntegerField(
                choices=[
                    (3, "Django-Model:ActiviteExceptionnel"),
                    (9, "Location batiments municipaux"),
                    (6, "Django-Model:AllocationPanneauPublicitaire"),
                    (10, "Django-Model:FoncierParcelle"),
                    (4, "Django-Model:VisiteSiteTouristique"),
                    (11, "Django-Model:VehiculeActivite"),
                    (16, "Django-Model:VehiculeActiviteDuplicata"),
                    (12, "Django-Model:VehiculeActivite"),
                    (15, "Django-Model:FoncierParcelleDuplicata"),
                    (2, "Django-Model:Marche"),
                    (17, "Django-Model:VehiculeProprietaireDuplicata"),
                    (7, "Django-Model:PubliciteMurCloture"),
                    (18, "Django-Model:BetailsPropriete"),
                    (8, "Django-Model:AllocationPlaceMarche"),
                    (1, "Django-Model:Standard"),
                    (5, "Django-Model:AllocationEspacePublique"),
                    (14, "Django-Model:BaseActiviteDuplicata"),
                    (13, "Django-Model:VehiculeProprietaire"),
                ],
                null=True,
            ),
        ),
        migrations.AlterField(
            model_name="noteimposition",
            name="entity",
            field=models.PositiveSmallIntegerField(
                choices=[
                    (3, "Django-Model:ActiviteExceptionnel"),
                    (9, "Location batiments municipaux"),
                    (6, "Django-Model:AllocationPanneauPublicitaire"),
                    (10, "Django-Model:FoncierParcelle"),
                    (4, "Django-Model:VisiteSiteTouristique"),
                    (11, "Django-Model:VehiculeActivite"),
                    (16, "Django-Model:VehiculeActiviteDuplicata"),
                    (12, "Django-Model:VehiculeActivite"),
                    (15, "Django-Model:FoncierParcelleDuplicata"),
                    (2, "Django-Model:Marche"),
                    (17, "Django-Model:VehiculeProprietaireDuplicata"),
                    (7, "Django-Model:PubliciteMurCloture"),
                    (18, "Django-Model:BetailsPropriete"),
                    (8, "Django-Model:AllocationPlaceMarche"),
                    (1, "Django-Model:Standard"),
                    (5, "Django-Model:AllocationEspacePublique"),
                    (14, "Django-Model:BaseActiviteDuplicata"),
                    (13, "Django-Model:VehiculeProprietaire"),
                ],
                null=True,
            ),
        ),
        migrations.AlterField(
            model_name="noteimpositiondelete",
            name="entity",
            field=models.PositiveSmallIntegerField(
                choices=[
                    (3, "Django-Model:ActiviteExceptionnel"),
                    (9, "Location batiments municipaux"),
                    (6, "Django-Model:AllocationPanneauPublicitaire"),
                    (10, "Django-Model:FoncierParcelle"),
                    (4, "Django-Model:VisiteSiteTouristique"),
                    (11, "Django-Model:VehiculeActivite"),
                    (16, "Django-Model:VehiculeActiviteDuplicata"),
                    (12, "Django-Model:VehiculeActivite"),
                    (15, "Django-Model:FoncierParcelleDuplicata"),
                    (2, "Django-Model:Marche"),
                    (17, "Django-Model:VehiculeProprietaireDuplicata"),
                    (7, "Django-Model:PubliciteMurCloture"),
                    (18, "Django-Model:BetailsPropriete"),
                    (8, "Django-Model:AllocationPlaceMarche"),
                    (1, "Django-Model:Standard"),
                    (5, "Django-Model:AllocationEspacePublique"),
                    (14, "Django-Model:BaseActiviteDuplicata"),
                    (13, "Django-Model:VehiculeProprietaire"),
                ],
                null=True,
            ),
        ),
        migrations.AlterField(
            model_name="periode",
            name="element",
            field=models.IntegerField(
                choices=[
                    (11, "NOVEMBRE"),
                    (7, "JUILLET"),
                    (15, "3e TRIMESTRE"),
                    (19, "ANNEE"),
                    (6, "JUIN"),
                    (13, "1er TRIMESTRE"),
                    (8, "AOUT"),
                    (4, "AVRIL"),
                    (2, "FEVRIER"),
                    (1, "JANVIER"),
                    (16, "4e TRIMESTRE"),
                    (12, "DECEMBRE"),
                    (3, "MARS"),
                    (10, "OCTOBRE"),
                    (9, "SEPTEMBRE"),
                    (5, "MAI"),
                    (14, "2e TRIMESTRE"),
                    (18, "2e SEMESTRE"),
                    (17, "1er SEMESTRE"),
                ],
                verbose_name="Elements de période",
            ),
        ),
        migrations.AlterField(
            model_name="periodetype",
            name="categorie",
            field=models.IntegerField(
                choices=[
                    (1, "Mensuelle"),
                    (3, "Semestrielle"),
                    (0, "Autre"),
                    (4, "Annuelle"),
                    (2, "Trimestrielle"),
                ],
                default=0,
                verbose_name="catégorie de périodes",
            ),
        ),
    ]
