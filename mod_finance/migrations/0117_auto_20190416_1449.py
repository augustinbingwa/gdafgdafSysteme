# Generated by Django 2.0.7 on 2019-04-16 12:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mod_finance', '0116_auto_20190325_1226'),
    ]

    operations = [
        migrations.AlterField(
            model_name='avisimposition',
            name='entity',
            field=models.PositiveSmallIntegerField(choices=[(4, 'Django-Model:VisiteSiteTouristique'), (17, 'Django-Model:VehiculeProprietaireDuplicata'), (7, 'Django-Model:PubliciteMurCloture'), (2, 'Django-Model:Marche'), (14, 'Django-Model:BaseActiviteDuplicata'), (11, 'Django-Model:VehiculeActivite'), (8, 'Django-Model:AllocationPlaceMarche'), (1, 'Django-Model:Standard'), (18, 'Django-Model:BetailsPropriete'), (10, 'Django-Model:FoncierParcelle'), (9, 'Location batiments municipaux'), (13, 'Django-Model:VehiculeProprietaire'), (6, 'Django-Model:AllocationPanneauPublicitaire'), (5, 'Django-Model:AllocationEspacePublique'), (15, 'Django-Model:FoncierParcelleDuplicata'), (3, 'Django-Model:ActiviteExceptionnel'), (12, 'Django-Model:VehiculeActivite'), (16, 'Django-Model:VehiculeActiviteDuplicata')], null=True),
        ),
        migrations.AlterField(
            model_name='avisimposition',
            name='entity_id',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='noteimposition',
            name='entity',
            field=models.PositiveSmallIntegerField(choices=[(4, 'Django-Model:VisiteSiteTouristique'), (17, 'Django-Model:VehiculeProprietaireDuplicata'), (7, 'Django-Model:PubliciteMurCloture'), (2, 'Django-Model:Marche'), (14, 'Django-Model:BaseActiviteDuplicata'), (11, 'Django-Model:VehiculeActivite'), (8, 'Django-Model:AllocationPlaceMarche'), (1, 'Django-Model:Standard'), (18, 'Django-Model:BetailsPropriete'), (10, 'Django-Model:FoncierParcelle'), (9, 'Location batiments municipaux'), (13, 'Django-Model:VehiculeProprietaire'), (6, 'Django-Model:AllocationPanneauPublicitaire'), (5, 'Django-Model:AllocationEspacePublique'), (15, 'Django-Model:FoncierParcelleDuplicata'), (3, 'Django-Model:ActiviteExceptionnel'), (12, 'Django-Model:VehiculeActivite'), (16, 'Django-Model:VehiculeActiviteDuplicata')], null=True),
        ),
        migrations.AlterField(
            model_name='noteimposition',
            name='entity_id',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='periode',
            name='element',
            field=models.IntegerField(choices=[(15, '3e TRIMESTRE'), (12, 'DECEMBRE'), (4, 'AVRIL'), (3, 'MARS'), (9, 'SEPTEMBRE'), (1, 'JANVIER'), (16, '4e TRIMESTRE'), (2, 'FEVRIER'), (17, '1er SEMESTRE'), (13, '1er TRIMESTRE'), (14, '2e TRIMESTRE'), (10, 'OCTOBRE'), (8, 'AOUT'), (5, 'MAI'), (19, 'ANNEE'), (18, '2e SEMESTRE'), (11, 'NOVEMBRE'), (7, 'JUILLET'), (6, 'JUIN')], verbose_name='Elements de période'),
        ),
        migrations.AlterField(
            model_name='periodetype',
            name='categorie',
            field=models.IntegerField(choices=[(1, 'Mensuelle'), (3, 'Semestrielle'), (4, 'Annuelle'), (2, 'Trimestrielle'), (0, 'Autre')], default=0, verbose_name='catégorie de périodes'),
        ),
    ]