# Generated by Django 2.0.7 on 2018-11-05 11:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mod_finance', '0032_auto_20181105_1029'),
    ]

    operations = [
        migrations.AlterField(
            model_name='avisimposition',
            name='entity',
            field=models.IntegerField(choices=[(18, 'Django-Model:BetailsPropriete'), (13, 'Django-Model:VehiculeProprietaire'), (7, 'Django-Model:PubliciteMurCloture'), (6, 'Django-Model:AllocationPanneauPublicitaire'), (16, 'Django-Model:VehiculeActiviteDuplicata'), (12, 'Django-Model:VehiculeActivite'), (10, 'Django-Model:FoncierParcelle'), (8, 'Django-Model:AllocationPlaceMarche'), (15, 'Django-Model:FoncierParcelleDuplicata'), (5, 'Django-Model:AllocationEspacePublique'), (3, 'Django-Model:ActiviteExceptionnel'), (17, 'Django-Model:VehiculeProprietaireDuplicata'), (2, 'Django-Model:Marche'), (14, 'Django-Model:BaseActiviteDuplicata'), (11, 'Django-Model:VehiculeActivite'), (4, 'Django-Model:VisiteSiteTouristique'), (1, 'Django-Model:Standard'), (9, 'Location batiments municipaux')], null=True),
        ),
        migrations.AlterField(
            model_name='noteimposition',
            name='entity',
            field=models.IntegerField(choices=[(18, 'Django-Model:BetailsPropriete'), (13, 'Django-Model:VehiculeProprietaire'), (7, 'Django-Model:PubliciteMurCloture'), (6, 'Django-Model:AllocationPanneauPublicitaire'), (16, 'Django-Model:VehiculeActiviteDuplicata'), (12, 'Django-Model:VehiculeActivite'), (10, 'Django-Model:FoncierParcelle'), (8, 'Django-Model:AllocationPlaceMarche'), (15, 'Django-Model:FoncierParcelleDuplicata'), (5, 'Django-Model:AllocationEspacePublique'), (3, 'Django-Model:ActiviteExceptionnel'), (17, 'Django-Model:VehiculeProprietaireDuplicata'), (2, 'Django-Model:Marche'), (14, 'Django-Model:BaseActiviteDuplicata'), (11, 'Django-Model:VehiculeActivite'), (4, 'Django-Model:VisiteSiteTouristique'), (1, 'Django-Model:Standard'), (9, 'Location batiments municipaux')], null=True),
        ),
        migrations.AlterField(
            model_name='periode',
            name='element',
            field=models.IntegerField(choices=[(12, 'Décembre'), (4, 'Avril'), (7, 'Juillet'), (11, 'Novembre'), (8, 'Août'), (6, 'Juin'), (10, 'Octobre'), (14, '2e Trimestre'), (3, 'Mars'), (1, 'Janvier'), (5, 'Mai'), (15, '3e Trimestre'), (17, '1er Semestre'), (9, 'Septembre'), (18, '2e Semestre'), (19, 'Année'), (2, 'Février'), (16, '4e Trimestre'), (13, '1er Trimestre')], verbose_name='Elements de période'),
        ),
        migrations.AlterField(
            model_name='periodetype',
            name='categorie',
            field=models.IntegerField(choices=[(2, 'Trimestrielle'), (1, 'Mensuelle'), (4, 'Annuelle'), (3, 'Semestrielle'), (0, 'Autre')], default=0, verbose_name='catégorie de périodes'),
        ),
    ]