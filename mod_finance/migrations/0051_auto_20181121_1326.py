# Generated by Django 2.0.7 on 2018-11-21 11:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mod_finance', '0050_auto_20181121_1311'),
    ]

    operations = [
        migrations.AlterField(
            model_name='avisimposition',
            name='entity',
            field=models.IntegerField(choices=[(3, 'Django-Model:ActiviteExceptionnel'), (4, 'Django-Model:VisiteSiteTouristique'), (9, 'Location batiments municipaux'), (7, 'Django-Model:PubliciteMurCloture'), (11, 'Django-Model:VehiculeActivite'), (16, 'Django-Model:VehiculeActiviteDuplicata'), (14, 'Django-Model:BaseActiviteDuplicata'), (18, 'Django-Model:BetailsPropriete'), (2, 'Django-Model:Marche'), (13, 'Django-Model:VehiculeProprietaire'), (10, 'Django-Model:FoncierParcelle'), (6, 'Django-Model:AllocationPanneauPublicitaire'), (17, 'Django-Model:VehiculeProprietaireDuplicata'), (12, 'Django-Model:VehiculeActivite'), (15, 'Django-Model:FoncierParcelleDuplicata'), (8, 'Django-Model:AllocationPlaceMarche'), (5, 'Django-Model:AllocationEspacePublique'), (1, 'Django-Model:Standard')], null=True),
        ),
        migrations.AlterField(
            model_name='noteimposition',
            name='entity',
            field=models.IntegerField(choices=[(3, 'Django-Model:ActiviteExceptionnel'), (4, 'Django-Model:VisiteSiteTouristique'), (9, 'Location batiments municipaux'), (7, 'Django-Model:PubliciteMurCloture'), (11, 'Django-Model:VehiculeActivite'), (16, 'Django-Model:VehiculeActiviteDuplicata'), (14, 'Django-Model:BaseActiviteDuplicata'), (18, 'Django-Model:BetailsPropriete'), (2, 'Django-Model:Marche'), (13, 'Django-Model:VehiculeProprietaire'), (10, 'Django-Model:FoncierParcelle'), (6, 'Django-Model:AllocationPanneauPublicitaire'), (17, 'Django-Model:VehiculeProprietaireDuplicata'), (12, 'Django-Model:VehiculeActivite'), (15, 'Django-Model:FoncierParcelleDuplicata'), (8, 'Django-Model:AllocationPlaceMarche'), (5, 'Django-Model:AllocationEspacePublique'), (1, 'Django-Model:Standard')], null=True),
        ),
        migrations.AlterField(
            model_name='periode',
            name='element',
            field=models.IntegerField(choices=[(12, 'Décembre'), (14, '2e Trimestre'), (9, 'Septembre'), (15, '3e Trimestre'), (2, 'Février'), (18, '2e Semestre'), (8, 'Août'), (10, 'Octobre'), (16, '4e Trimestre'), (4, 'Avril'), (5, 'Mai'), (6, 'Juin'), (13, '1er Trimestre'), (17, '1er Semestre'), (19, 'Année'), (7, 'Juillet'), (1, 'Janvier'), (11, 'Novembre'), (3, 'Mars')], verbose_name='Elements de période'),
        ),
        migrations.AlterField(
            model_name='periodetype',
            name='categorie',
            field=models.IntegerField(choices=[(4, 'Annuelle'), (2, 'Trimestrielle'), (0, 'Autre'), (3, 'Semestrielle'), (1, 'Mensuelle')], default=0, verbose_name='catégorie de périodes'),
        ),
    ]
