# Generated by Django 2.0.7 on 2019-01-07 21:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mod_finance', '0073_auto_20190106_1750'),
    ]

    operations = [
        migrations.AlterField(
            model_name='avisimposition',
            name='entity',
            field=models.IntegerField(choices=[(13, 'Django-Model:VehiculeProprietaire'), (7, 'Django-Model:PubliciteMurCloture'), (8, 'Django-Model:AllocationPlaceMarche'), (10, 'Django-Model:FoncierParcelle'), (15, 'Django-Model:FoncierParcelleDuplicata'), (9, 'Location batiments municipaux'), (4, 'Django-Model:VisiteSiteTouristique'), (3, 'Django-Model:ActiviteExceptionnel'), (11, 'Django-Model:VehiculeActivite'), (17, 'Django-Model:VehiculeProprietaireDuplicata'), (16, 'Django-Model:VehiculeActiviteDuplicata'), (1, 'Django-Model:Standard'), (6, 'Django-Model:AllocationPanneauPublicitaire'), (12, 'Django-Model:VehiculeActivite'), (2, 'Django-Model:Marche'), (5, 'Django-Model:AllocationEspacePublique'), (18, 'Django-Model:BetailsPropriete'), (14, 'Django-Model:BaseActiviteDuplicata')], null=True),
        ),
        migrations.AlterField(
            model_name='noteimposition',
            name='entity',
            field=models.IntegerField(choices=[(13, 'Django-Model:VehiculeProprietaire'), (7, 'Django-Model:PubliciteMurCloture'), (8, 'Django-Model:AllocationPlaceMarche'), (10, 'Django-Model:FoncierParcelle'), (15, 'Django-Model:FoncierParcelleDuplicata'), (9, 'Location batiments municipaux'), (4, 'Django-Model:VisiteSiteTouristique'), (3, 'Django-Model:ActiviteExceptionnel'), (11, 'Django-Model:VehiculeActivite'), (17, 'Django-Model:VehiculeProprietaireDuplicata'), (16, 'Django-Model:VehiculeActiviteDuplicata'), (1, 'Django-Model:Standard'), (6, 'Django-Model:AllocationPanneauPublicitaire'), (12, 'Django-Model:VehiculeActivite'), (2, 'Django-Model:Marche'), (5, 'Django-Model:AllocationEspacePublique'), (18, 'Django-Model:BetailsPropriete'), (14, 'Django-Model:BaseActiviteDuplicata')], null=True),
        ),
        migrations.AlterField(
            model_name='periode',
            name='element',
            field=models.IntegerField(choices=[(1, 'Janvier'), (8, 'Août'), (4, 'Avril'), (12, 'Décembre'), (14, '2e Trimestre'), (9, 'Septembre'), (19, 'Année'), (16, '4e Trimestre'), (15, '3e Trimestre'), (18, '2e Semestre'), (6, 'Juin'), (7, 'Juillet'), (11, 'Novembre'), (13, '1er Trimestre'), (17, '1er Semestre'), (3, 'Mars'), (2, 'Février'), (5, 'Mai'), (10, 'Octobre')], verbose_name='Elements de période'),
        ),
        migrations.AlterField(
            model_name='periodetype',
            name='categorie',
            field=models.IntegerField(choices=[(3, 'Semestrielle'), (0, 'Autre'), (1, 'Mensuelle'), (4, 'Annuelle'), (2, 'Trimestrielle')], default=0, verbose_name='catégorie de périodes'),
        ),
    ]
