# Generated by Django 2.0.7 on 2019-01-18 14:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mod_finance', '0095_auto_20190117_1948'),
    ]

    operations = [
        migrations.AlterField(
            model_name='avisimposition',
            name='entity',
            field=models.IntegerField(choices=[(10, 'Django-Model:FoncierParcelle'), (1, 'Django-Model:Standard'), (13, 'Django-Model:VehiculeProprietaire'), (16, 'Django-Model:VehiculeActiviteDuplicata'), (14, 'Django-Model:BaseActiviteDuplicata'), (6, 'Django-Model:AllocationPanneauPublicitaire'), (9, 'Location batiments municipaux'), (8, 'Django-Model:AllocationPlaceMarche'), (11, 'Django-Model:VehiculeActivite'), (3, 'Django-Model:ActiviteExceptionnel'), (7, 'Django-Model:PubliciteMurCloture'), (5, 'Django-Model:AllocationEspacePublique'), (4, 'Django-Model:VisiteSiteTouristique'), (15, 'Django-Model:FoncierParcelleDuplicata'), (12, 'Django-Model:VehiculeActivite'), (2, 'Django-Model:Marche'), (18, 'Django-Model:BetailsPropriete'), (17, 'Django-Model:VehiculeProprietaireDuplicata')], null=True),
        ),
        migrations.AlterField(
            model_name='noteimposition',
            name='entity',
            field=models.IntegerField(choices=[(10, 'Django-Model:FoncierParcelle'), (1, 'Django-Model:Standard'), (13, 'Django-Model:VehiculeProprietaire'), (16, 'Django-Model:VehiculeActiviteDuplicata'), (14, 'Django-Model:BaseActiviteDuplicata'), (6, 'Django-Model:AllocationPanneauPublicitaire'), (9, 'Location batiments municipaux'), (8, 'Django-Model:AllocationPlaceMarche'), (11, 'Django-Model:VehiculeActivite'), (3, 'Django-Model:ActiviteExceptionnel'), (7, 'Django-Model:PubliciteMurCloture'), (5, 'Django-Model:AllocationEspacePublique'), (4, 'Django-Model:VisiteSiteTouristique'), (15, 'Django-Model:FoncierParcelleDuplicata'), (12, 'Django-Model:VehiculeActivite'), (2, 'Django-Model:Marche'), (18, 'Django-Model:BetailsPropriete'), (17, 'Django-Model:VehiculeProprietaireDuplicata')], null=True),
        ),
        migrations.AlterField(
            model_name='periode',
            name='element',
            field=models.IntegerField(choices=[(16, '4e Trimestre'), (3, 'Mars'), (1, 'Janvier'), (8, 'Août'), (5, 'Mai'), (2, 'Février'), (12, 'Décembre'), (9, 'Septembre'), (15, '3e Trimestre'), (13, '1er Trimestre'), (10, 'Octobre'), (19, 'Année'), (17, '1er Semestre'), (18, '2e Semestre'), (11, 'Novembre'), (7, 'Juillet'), (6, 'Juin'), (14, '2e Trimestre'), (4, 'Avril')], verbose_name='Elements de période'),
        ),
        migrations.AlterField(
            model_name='periodetype',
            name='categorie',
            field=models.IntegerField(choices=[(4, 'Annuelle'), (2, 'Trimestrielle'), (3, 'Semestrielle'), (0, 'Autre'), (1, 'Mensuelle')], default=0, verbose_name='catégorie de périodes'),
        ),
        migrations.AlterUniqueTogether(
            name='noteimposition',
            unique_together={('entity', 'entity_id', 'periode', 'annee')},
        ),
        migrations.AlterIndexTogether(
            name='noteimposition',
            index_together={('entity', 'entity_id', 'periode', 'annee')},
        ),
    ]