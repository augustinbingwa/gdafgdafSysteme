# Generated by Django 2.0.7 on 2018-10-31 15:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mod_finance', '0023_auto_20181031_1045'),
    ]

    operations = [
        migrations.AlterField(
            model_name='avisimposition',
            name='entity',
            field=models.IntegerField(choices=[(14, 'Django-Model:BaseActiviteDuplicata'), (4, 'Django-Model:VisiteSiteTouristique'), (11, 'Django-Model:VehiculeActivite'), (2, 'Django-Model:Marche'), (9, 'Location batiments municipaux'), (1, 'Django-Model:Standard'), (6, 'Django-Model:AllocationPanneauPublicitaire'), (15, 'Django-Model:FoncierParcelleDuplicata'), (12, 'Django-Model:VehiculeActivite'), (7, 'Django-Model:PubliciteMurCloture'), (8, 'Django-Model:AllocationPlaceMarche'), (16, 'Django-Model:VehiculeActiviteDuplicata'), (13, 'Django-Model:VehiculeProprietaire'), (17, 'Django-Model:VehiculeProprietaireDuplicata'), (5, 'Django-Model:AllocationEspacePublique'), (10, 'Django-Model:FoncierParcelle'), (3, 'Django-Model:ActiviteExceptionnel'), (18, 'Django-Model:BetailsPropriete')], null=True),
        ),
        migrations.AlterField(
            model_name='noteimposition',
            name='entity',
            field=models.IntegerField(choices=[(14, 'Django-Model:BaseActiviteDuplicata'), (4, 'Django-Model:VisiteSiteTouristique'), (11, 'Django-Model:VehiculeActivite'), (2, 'Django-Model:Marche'), (9, 'Location batiments municipaux'), (1, 'Django-Model:Standard'), (6, 'Django-Model:AllocationPanneauPublicitaire'), (15, 'Django-Model:FoncierParcelleDuplicata'), (12, 'Django-Model:VehiculeActivite'), (7, 'Django-Model:PubliciteMurCloture'), (8, 'Django-Model:AllocationPlaceMarche'), (16, 'Django-Model:VehiculeActiviteDuplicata'), (13, 'Django-Model:VehiculeProprietaire'), (17, 'Django-Model:VehiculeProprietaireDuplicata'), (5, 'Django-Model:AllocationEspacePublique'), (10, 'Django-Model:FoncierParcelle'), (3, 'Django-Model:ActiviteExceptionnel'), (18, 'Django-Model:BetailsPropriete')], null=True),
        ),
        migrations.AlterField(
            model_name='periode',
            name='element',
            field=models.IntegerField(choices=[(11, 'Novembre'), (16, '4e Timestre'), (13, '1er Trimestre'), (14, '2e Trimestre'), (17, '1er Semestre'), (18, '2e Semestre'), (3, 'Mars'), (10, 'Octobre'), (19, 'Année'), (2, 'Février'), (7, 'Juillet'), (12, 'Décembre'), (5, 'Mai'), (4, 'Avril'), (9, 'Septembre'), (1, 'Janvier'), (6, 'Juin'), (8, 'Août'), (15, '3e Trimestre')], verbose_name='Elements de période'),
        ),
        migrations.AlterField(
            model_name='periodetype',
            name='categorie',
            field=models.IntegerField(choices=[(4, 'Annuelle'), (1, 'Mensuelle'), (2, 'Trimestrielle'), (0, 'Autre'), (3, 'Semestrielle')], default=0, verbose_name='catégorie de périodes'),
        ),
    ]
