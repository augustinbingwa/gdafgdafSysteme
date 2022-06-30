# Generated by Django 2.0.7 on 2019-01-11 06:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mod_finance', '0085_auto_20190111_0803'),
    ]

    operations = [
        migrations.AlterField(
            model_name='avisimposition',
            name='entity',
            field=models.IntegerField(choices=[(17, 'Django-Model:VehiculeProprietaireDuplicata'), (1, 'Django-Model:Standard'), (6, 'Django-Model:AllocationPanneauPublicitaire'), (4, 'Django-Model:VisiteSiteTouristique'), (7, 'Django-Model:PubliciteMurCloture'), (11, 'Django-Model:VehiculeActivite'), (15, 'Django-Model:FoncierParcelleDuplicata'), (16, 'Django-Model:VehiculeActiviteDuplicata'), (8, 'Django-Model:AllocationPlaceMarche'), (13, 'Django-Model:VehiculeProprietaire'), (2, 'Django-Model:Marche'), (12, 'Django-Model:VehiculeActivite'), (10, 'Django-Model:FoncierParcelle'), (18, 'Django-Model:BetailsPropriete'), (5, 'Django-Model:AllocationEspacePublique'), (14, 'Django-Model:BaseActiviteDuplicata'), (9, 'Location batiments municipaux'), (3, 'Django-Model:ActiviteExceptionnel')], null=True),
        ),
        migrations.AlterField(
            model_name='noteimposition',
            name='entity',
            field=models.IntegerField(choices=[(17, 'Django-Model:VehiculeProprietaireDuplicata'), (1, 'Django-Model:Standard'), (6, 'Django-Model:AllocationPanneauPublicitaire'), (4, 'Django-Model:VisiteSiteTouristique'), (7, 'Django-Model:PubliciteMurCloture'), (11, 'Django-Model:VehiculeActivite'), (15, 'Django-Model:FoncierParcelleDuplicata'), (16, 'Django-Model:VehiculeActiviteDuplicata'), (8, 'Django-Model:AllocationPlaceMarche'), (13, 'Django-Model:VehiculeProprietaire'), (2, 'Django-Model:Marche'), (12, 'Django-Model:VehiculeActivite'), (10, 'Django-Model:FoncierParcelle'), (18, 'Django-Model:BetailsPropriete'), (5, 'Django-Model:AllocationEspacePublique'), (14, 'Django-Model:BaseActiviteDuplicata'), (9, 'Location batiments municipaux'), (3, 'Django-Model:ActiviteExceptionnel')], null=True),
        ),
        migrations.AlterField(
            model_name='periode',
            name='element',
            field=models.IntegerField(choices=[(7, 'Juillet'), (2, 'Février'), (10, 'Octobre'), (1, 'Janvier'), (13, '1er Trimestre'), (16, '4e Trimestre'), (19, 'Année'), (18, '2e Semestre'), (9, 'Septembre'), (5, 'Mai'), (15, '3e Trimestre'), (12, 'Décembre'), (4, 'Avril'), (8, 'Août'), (11, 'Novembre'), (17, '1er Semestre'), (3, 'Mars'), (6, 'Juin'), (14, '2e Trimestre')], verbose_name='Elements de période'),
        ),
        migrations.AlterField(
            model_name='periodetype',
            name='categorie',
            field=models.IntegerField(choices=[(2, 'Trimestrielle'), (0, 'Autre'), (3, 'Semestrielle'), (4, 'Annuelle'), (1, 'Mensuelle')], default=0, verbose_name='catégorie de périodes'),
        ),
    ]