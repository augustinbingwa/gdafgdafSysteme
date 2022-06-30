# Generated by Django 2.0.7 on 2018-11-15 16:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mod_finance', '0045_auto_20181115_1758'),
    ]

    operations = [
        migrations.AlterField(
            model_name='avisimposition',
            name='entity',
            field=models.IntegerField(choices=[(9, 'Location batiments municipaux'), (13, 'Django-Model:VehiculeProprietaire'), (12, 'Django-Model:VehiculeActivite'), (15, 'Django-Model:FoncierParcelleDuplicata'), (1, 'Django-Model:Standard'), (2, 'Django-Model:Marche'), (7, 'Django-Model:PubliciteMurCloture'), (18, 'Django-Model:BetailsPropriete'), (3, 'Django-Model:ActiviteExceptionnel'), (5, 'Django-Model:AllocationEspacePublique'), (6, 'Django-Model:AllocationPanneauPublicitaire'), (10, 'Django-Model:FoncierParcelle'), (14, 'Django-Model:BaseActiviteDuplicata'), (17, 'Django-Model:VehiculeProprietaireDuplicata'), (11, 'Django-Model:VehiculeActivite'), (8, 'Django-Model:AllocationPlaceMarche'), (4, 'Django-Model:VisiteSiteTouristique'), (16, 'Django-Model:VehiculeActiviteDuplicata')], null=True),
        ),
        migrations.AlterField(
            model_name='noteimposition',
            name='entity',
            field=models.IntegerField(choices=[(9, 'Location batiments municipaux'), (13, 'Django-Model:VehiculeProprietaire'), (12, 'Django-Model:VehiculeActivite'), (15, 'Django-Model:FoncierParcelleDuplicata'), (1, 'Django-Model:Standard'), (2, 'Django-Model:Marche'), (7, 'Django-Model:PubliciteMurCloture'), (18, 'Django-Model:BetailsPropriete'), (3, 'Django-Model:ActiviteExceptionnel'), (5, 'Django-Model:AllocationEspacePublique'), (6, 'Django-Model:AllocationPanneauPublicitaire'), (10, 'Django-Model:FoncierParcelle'), (14, 'Django-Model:BaseActiviteDuplicata'), (17, 'Django-Model:VehiculeProprietaireDuplicata'), (11, 'Django-Model:VehiculeActivite'), (8, 'Django-Model:AllocationPlaceMarche'), (4, 'Django-Model:VisiteSiteTouristique'), (16, 'Django-Model:VehiculeActiviteDuplicata')], null=True),
        ),
        migrations.AlterField(
            model_name='periode',
            name='element',
            field=models.IntegerField(choices=[(4, 'Avril'), (9, 'Septembre'), (8, 'Août'), (17, '1er Semestre'), (2, 'Février'), (15, '3e Trimestre'), (13, '1er Trimestre'), (19, 'Année'), (14, '2e Trimestre'), (18, '2e Semestre'), (7, 'Juillet'), (3, 'Mars'), (10, 'Octobre'), (5, 'Mai'), (11, 'Novembre'), (6, 'Juin'), (16, '4e Trimestre'), (12, 'Décembre'), (1, 'Janvier')], verbose_name='Elements de période'),
        ),
        migrations.AlterField(
            model_name='periodetype',
            name='categorie',
            field=models.IntegerField(choices=[(2, 'Trimestrielle'), (0, 'Autre'), (3, 'Semestrielle'), (1, 'Mensuelle'), (4, 'Annuelle')], default=0, verbose_name='catégorie de périodes'),
        ),
    ]
