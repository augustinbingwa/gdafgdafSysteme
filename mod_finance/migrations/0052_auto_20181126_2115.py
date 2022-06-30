# Generated by Django 2.0.7 on 2018-11-26 19:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mod_finance', '0051_auto_20181121_1326'),
    ]

    operations = [
        migrations.AlterField(
            model_name='avisimposition',
            name='entity',
            field=models.IntegerField(choices=[(8, 'Django-Model:AllocationPlaceMarche'), (6, 'Django-Model:AllocationPanneauPublicitaire'), (4, 'Django-Model:VisiteSiteTouristique'), (1, 'Django-Model:Standard'), (10, 'Django-Model:FoncierParcelle'), (2, 'Django-Model:Marche'), (5, 'Django-Model:AllocationEspacePublique'), (13, 'Django-Model:VehiculeProprietaire'), (3, 'Django-Model:ActiviteExceptionnel'), (17, 'Django-Model:VehiculeProprietaireDuplicata'), (12, 'Django-Model:VehiculeActivite'), (15, 'Django-Model:FoncierParcelleDuplicata'), (7, 'Django-Model:PubliciteMurCloture'), (9, 'Location batiments municipaux'), (14, 'Django-Model:BaseActiviteDuplicata'), (16, 'Django-Model:VehiculeActiviteDuplicata'), (18, 'Django-Model:BetailsPropriete'), (11, 'Django-Model:VehiculeActivite')], null=True),
        ),
        migrations.AlterField(
            model_name='noteimposition',
            name='entity',
            field=models.IntegerField(choices=[(8, 'Django-Model:AllocationPlaceMarche'), (6, 'Django-Model:AllocationPanneauPublicitaire'), (4, 'Django-Model:VisiteSiteTouristique'), (1, 'Django-Model:Standard'), (10, 'Django-Model:FoncierParcelle'), (2, 'Django-Model:Marche'), (5, 'Django-Model:AllocationEspacePublique'), (13, 'Django-Model:VehiculeProprietaire'), (3, 'Django-Model:ActiviteExceptionnel'), (17, 'Django-Model:VehiculeProprietaireDuplicata'), (12, 'Django-Model:VehiculeActivite'), (15, 'Django-Model:FoncierParcelleDuplicata'), (7, 'Django-Model:PubliciteMurCloture'), (9, 'Location batiments municipaux'), (14, 'Django-Model:BaseActiviteDuplicata'), (16, 'Django-Model:VehiculeActiviteDuplicata'), (18, 'Django-Model:BetailsPropriete'), (11, 'Django-Model:VehiculeActivite')], null=True),
        ),
        migrations.AlterField(
            model_name='periode',
            name='element',
            field=models.IntegerField(choices=[(11, 'Novembre'), (15, '3e Trimestre'), (4, 'Avril'), (18, '2e Semestre'), (7, 'Juillet'), (9, 'Septembre'), (12, 'Décembre'), (2, 'Février'), (1, 'Janvier'), (10, 'Octobre'), (6, 'Juin'), (13, '1er Trimestre'), (3, 'Mars'), (19, 'Année'), (16, '4e Trimestre'), (8, 'Août'), (17, '1er Semestre'), (5, 'Mai'), (14, '2e Trimestre')], verbose_name='Elements de période'),
        ),
        migrations.AlterField(
            model_name='periodetype',
            name='categorie',
            field=models.IntegerField(choices=[(2, 'Trimestrielle'), (1, 'Mensuelle'), (4, 'Annuelle'), (3, 'Semestrielle'), (0, 'Autre')], default=0, verbose_name='catégorie de périodes'),
        ),
    ]
