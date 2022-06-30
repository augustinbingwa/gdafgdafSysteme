# Generated by Django 2.0.7 on 2019-02-28 06:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mod_finance', '0113_auto_20190227_2015'),
    ]

    operations = [
        migrations.AlterField(
            model_name='avisimposition',
            name='entity',
            field=models.IntegerField(choices=[(7, 'Django-Model:PubliciteMurCloture'), (11, 'Django-Model:VehiculeActivite'), (16, 'Django-Model:VehiculeActiviteDuplicata'), (18, 'Django-Model:BetailsPropriete'), (17, 'Django-Model:VehiculeProprietaireDuplicata'), (10, 'Django-Model:FoncierParcelle'), (13, 'Django-Model:VehiculeProprietaire'), (14, 'Django-Model:BaseActiviteDuplicata'), (9, 'Location batiments municipaux'), (3, 'Django-Model:ActiviteExceptionnel'), (1, 'Django-Model:Standard'), (2, 'Django-Model:Marche'), (8, 'Django-Model:AllocationPlaceMarche'), (5, 'Django-Model:AllocationEspacePublique'), (12, 'Django-Model:VehiculeActivite'), (6, 'Django-Model:AllocationPanneauPublicitaire'), (15, 'Django-Model:FoncierParcelleDuplicata'), (4, 'Django-Model:VisiteSiteTouristique')], null=True),
        ),
        migrations.AlterField(
            model_name='noteimposition',
            name='entity',
            field=models.IntegerField(choices=[(7, 'Django-Model:PubliciteMurCloture'), (11, 'Django-Model:VehiculeActivite'), (16, 'Django-Model:VehiculeActiviteDuplicata'), (18, 'Django-Model:BetailsPropriete'), (17, 'Django-Model:VehiculeProprietaireDuplicata'), (10, 'Django-Model:FoncierParcelle'), (13, 'Django-Model:VehiculeProprietaire'), (14, 'Django-Model:BaseActiviteDuplicata'), (9, 'Location batiments municipaux'), (3, 'Django-Model:ActiviteExceptionnel'), (1, 'Django-Model:Standard'), (2, 'Django-Model:Marche'), (8, 'Django-Model:AllocationPlaceMarche'), (5, 'Django-Model:AllocationEspacePublique'), (12, 'Django-Model:VehiculeActivite'), (6, 'Django-Model:AllocationPanneauPublicitaire'), (15, 'Django-Model:FoncierParcelleDuplicata'), (4, 'Django-Model:VisiteSiteTouristique')], null=True),
        ),
        migrations.AlterField(
            model_name='periode',
            name='element',
            field=models.IntegerField(choices=[(14, '2e Trimestre'), (3, 'Mars'), (5, 'Mai'), (1, 'Janvier'), (9, 'Septembre'), (7, 'Juillet'), (16, '4e Trimestre'), (4, 'Avril'), (18, '2e Semestre'), (11, 'Novembre'), (8, 'Août'), (17, '1er Semestre'), (15, '3e Trimestre'), (2, 'Février'), (13, '1er Trimestre'), (10, 'Octobre'), (19, 'Année'), (6, 'Juin'), (12, 'Décembre')], verbose_name='Elements de période'),
        ),
        migrations.AlterField(
            model_name='periodetype',
            name='categorie',
            field=models.IntegerField(choices=[(1, 'Mensuelle'), (2, 'Trimestrielle'), (4, 'Annuelle'), (3, 'Semestrielle'), (0, 'Autre')], default=0, verbose_name='catégorie de périodes'),
        ),
    ]