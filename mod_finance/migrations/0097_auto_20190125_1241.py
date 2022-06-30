# Generated by Django 2.0.7 on 2019-01-25 10:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mod_finance', '0096_auto_20190118_1650'),
    ]

    operations = [
        migrations.AlterField(
            model_name='avisimposition',
            name='entity',
            field=models.IntegerField(choices=[(15, 'Django-Model:FoncierParcelleDuplicata'), (14, 'Django-Model:BaseActiviteDuplicata'), (12, 'Django-Model:VehiculeActivite'), (3, 'Django-Model:ActiviteExceptionnel'), (2, 'Django-Model:Marche'), (6, 'Django-Model:AllocationPanneauPublicitaire'), (13, 'Django-Model:VehiculeProprietaire'), (5, 'Django-Model:AllocationEspacePublique'), (10, 'Django-Model:FoncierParcelle'), (16, 'Django-Model:VehiculeActiviteDuplicata'), (17, 'Django-Model:VehiculeProprietaireDuplicata'), (9, 'Location batiments municipaux'), (11, 'Django-Model:VehiculeActivite'), (1, 'Django-Model:Standard'), (18, 'Django-Model:BetailsPropriete'), (7, 'Django-Model:PubliciteMurCloture'), (8, 'Django-Model:AllocationPlaceMarche'), (4, 'Django-Model:VisiteSiteTouristique')], null=True),
        ),
        migrations.AlterField(
            model_name='noteimposition',
            name='entity',
            field=models.IntegerField(choices=[(15, 'Django-Model:FoncierParcelleDuplicata'), (14, 'Django-Model:BaseActiviteDuplicata'), (12, 'Django-Model:VehiculeActivite'), (3, 'Django-Model:ActiviteExceptionnel'), (2, 'Django-Model:Marche'), (6, 'Django-Model:AllocationPanneauPublicitaire'), (13, 'Django-Model:VehiculeProprietaire'), (5, 'Django-Model:AllocationEspacePublique'), (10, 'Django-Model:FoncierParcelle'), (16, 'Django-Model:VehiculeActiviteDuplicata'), (17, 'Django-Model:VehiculeProprietaireDuplicata'), (9, 'Location batiments municipaux'), (11, 'Django-Model:VehiculeActivite'), (1, 'Django-Model:Standard'), (18, 'Django-Model:BetailsPropriete'), (7, 'Django-Model:PubliciteMurCloture'), (8, 'Django-Model:AllocationPlaceMarche'), (4, 'Django-Model:VisiteSiteTouristique')], null=True),
        ),
        migrations.AlterField(
            model_name='periode',
            name='element',
            field=models.IntegerField(choices=[(1, 'Janvier'), (6, 'Juin'), (11, 'Novembre'), (2, 'Février'), (17, '1er Semestre'), (13, '1er Trimestre'), (9, 'Septembre'), (10, 'Octobre'), (7, 'Juillet'), (16, '4e Trimestre'), (18, '2e Semestre'), (19, 'Année'), (3, 'Mars'), (4, 'Avril'), (15, '3e Trimestre'), (5, 'Mai'), (14, '2e Trimestre'), (12, 'Décembre'), (8, 'Août')], verbose_name='Elements de période'),
        ),
        migrations.AlterField(
            model_name='periodetype',
            name='categorie',
            field=models.IntegerField(choices=[(1, 'Mensuelle'), (2, 'Trimestrielle'), (3, 'Semestrielle'), (4, 'Annuelle'), (0, 'Autre')], default=0, verbose_name='catégorie de périodes'),
        ),
    ]