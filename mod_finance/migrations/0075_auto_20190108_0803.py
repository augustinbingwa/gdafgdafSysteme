# Generated by Django 2.0.7 on 2019-01-08 06:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mod_finance', '0074_auto_20190107_2340'),
    ]

    operations = [
        migrations.AlterField(
            model_name='avisimposition',
            name='entity',
            field=models.IntegerField(choices=[(1, 'Django-Model:Standard'), (15, 'Django-Model:FoncierParcelleDuplicata'), (12, 'Django-Model:VehiculeActivite'), (10, 'Django-Model:FoncierParcelle'), (17, 'Django-Model:VehiculeProprietaireDuplicata'), (5, 'Django-Model:AllocationEspacePublique'), (3, 'Django-Model:ActiviteExceptionnel'), (9, 'Location batiments municipaux'), (6, 'Django-Model:AllocationPanneauPublicitaire'), (16, 'Django-Model:VehiculeActiviteDuplicata'), (7, 'Django-Model:PubliciteMurCloture'), (4, 'Django-Model:VisiteSiteTouristique'), (11, 'Django-Model:VehiculeActivite'), (8, 'Django-Model:AllocationPlaceMarche'), (13, 'Django-Model:VehiculeProprietaire'), (14, 'Django-Model:BaseActiviteDuplicata'), (2, 'Django-Model:Marche'), (18, 'Django-Model:BetailsPropriete')], null=True),
        ),
        migrations.AlterField(
            model_name='noteimposition',
            name='entity',
            field=models.IntegerField(choices=[(1, 'Django-Model:Standard'), (15, 'Django-Model:FoncierParcelleDuplicata'), (12, 'Django-Model:VehiculeActivite'), (10, 'Django-Model:FoncierParcelle'), (17, 'Django-Model:VehiculeProprietaireDuplicata'), (5, 'Django-Model:AllocationEspacePublique'), (3, 'Django-Model:ActiviteExceptionnel'), (9, 'Location batiments municipaux'), (6, 'Django-Model:AllocationPanneauPublicitaire'), (16, 'Django-Model:VehiculeActiviteDuplicata'), (7, 'Django-Model:PubliciteMurCloture'), (4, 'Django-Model:VisiteSiteTouristique'), (11, 'Django-Model:VehiculeActivite'), (8, 'Django-Model:AllocationPlaceMarche'), (13, 'Django-Model:VehiculeProprietaire'), (14, 'Django-Model:BaseActiviteDuplicata'), (2, 'Django-Model:Marche'), (18, 'Django-Model:BetailsPropriete')], null=True),
        ),
        migrations.AlterField(
            model_name='periode',
            name='element',
            field=models.IntegerField(choices=[(1, 'Janvier'), (13, '1er Trimestre'), (18, '2e Semestre'), (4, 'Avril'), (14, '2e Trimestre'), (5, 'Mai'), (2, 'Février'), (9, 'Septembre'), (7, 'Juillet'), (11, 'Novembre'), (12, 'Décembre'), (15, '3e Trimestre'), (19, 'Année'), (3, 'Mars'), (16, '4e Trimestre'), (17, '1er Semestre'), (10, 'Octobre'), (8, 'Août'), (6, 'Juin')], verbose_name='Elements de période'),
        ),
        migrations.AlterField(
            model_name='periodetype',
            name='categorie',
            field=models.IntegerField(choices=[(0, 'Autre'), (4, 'Annuelle'), (2, 'Trimestrielle'), (1, 'Mensuelle'), (3, 'Semestrielle')], default=0, verbose_name='catégorie de périodes'),
        ),
    ]
