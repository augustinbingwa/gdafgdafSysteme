# Generated by Django 2.0.7 on 2018-10-29 07:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mod_finance', '0017_auto_20181029_0824'),
    ]

    operations = [
        migrations.AlterField(
            model_name='avisimposition',
            name='entity',
            field=models.IntegerField(choices=[(3, 'Django-Model:ActiviteExceptionnel'), (5, 'Django-Model:AllocationEspacePublique'), (1, 'Django-Model:Standard'), (10, 'Django-Model:FoncierParcelle'), (12, 'Django-Model:VehiculeActivite'), (18, 'Django-Model:BetailsPropriete'), (6, 'Django-Model:AllocationPanneauPublicitaire'), (13, 'Django-Model:VehiculeProprietaire'), (8, 'Django-Model:AllocationPlaceMarche'), (9, 'Location batiments municipaux'), (16, 'Django-Model:VehiculeActiviteDuplicata'), (2, 'Django-Model:Marche'), (7, 'Django-Model:PubliciteMurCloture'), (15, 'Django-Model:FoncierParcelleDuplicata'), (11, 'Django-Model:VehiculeActivite'), (17, 'Django-Model:VehiculeProprietaireDuplicata'), (4, 'Django-Model:VisiteSiteTouristique'), (14, 'Django-Model:BaseActiviteDuplicata')], null=True),
        ),
        migrations.AlterField(
            model_name='noteimposition',
            name='entity',
            field=models.IntegerField(choices=[(3, 'Django-Model:ActiviteExceptionnel'), (5, 'Django-Model:AllocationEspacePublique'), (1, 'Django-Model:Standard'), (10, 'Django-Model:FoncierParcelle'), (12, 'Django-Model:VehiculeActivite'), (18, 'Django-Model:BetailsPropriete'), (6, 'Django-Model:AllocationPanneauPublicitaire'), (13, 'Django-Model:VehiculeProprietaire'), (8, 'Django-Model:AllocationPlaceMarche'), (9, 'Location batiments municipaux'), (16, 'Django-Model:VehiculeActiviteDuplicata'), (2, 'Django-Model:Marche'), (7, 'Django-Model:PubliciteMurCloture'), (15, 'Django-Model:FoncierParcelleDuplicata'), (11, 'Django-Model:VehiculeActivite'), (17, 'Django-Model:VehiculeProprietaireDuplicata'), (4, 'Django-Model:VisiteSiteTouristique'), (14, 'Django-Model:BaseActiviteDuplicata')], null=True),
        ),
        migrations.AlterField(
            model_name='periode',
            name='element',
            field=models.IntegerField(choices=[(19, 'Année'), (1, 'Janvier'), (9, 'Septembre'), (11, 'Novembre'), (5, 'Mai'), (13, '1er Trimestre'), (14, '2e Trimestre'), (16, '4e Timestre'), (17, '1er Semestre'), (12, 'Décembre'), (10, 'Octobre'), (18, '2e Semestre'), (8, 'Août'), (15, '3e Trimestre'), (4, 'Avril'), (3, 'Mars'), (2, 'Février'), (6, 'Juin'), (7, 'Juillet')], verbose_name='Elements de période'),
        ),
        migrations.AlterField(
            model_name='periodetype',
            name='categorie',
            field=models.IntegerField(choices=[(3, 'Semestrielle'), (2, 'Trimestrielle'), (1, 'Mensuelle'), (0, 'Autre'), (4, 'Annuelle')], default=0, verbose_name='catégorie de périodes'),
        ),
    ]