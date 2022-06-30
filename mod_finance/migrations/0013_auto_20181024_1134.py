# Generated by Django 2.0.7 on 2018-10-24 09:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mod_finance', '0012_auto_20181024_1052'),
    ]

    operations = [
        migrations.AlterField(
            model_name='avisimposition',
            name='entity',
            field=models.IntegerField(choices=[(13, 'Django-Model:VehiculeProprietaire'), (3, 'Django-Model:ActiviteExceptionnel'), (11, 'Django-Model:VehiculeActivite'), (2, 'Django-Model:Marche'), (6, 'Django-Model:AllocationPanneauPublicitaire'), (9, 'Location batiments municipaux'), (10, 'Django-Model:FoncierParcelle'), (8, 'Django-Model:AllocationPlaceMarche'), (16, 'Django-Model:VehiculeActiviteDuplicata'), (1, 'Django-Model:Standard'), (7, 'Django-Model:PubliciteMurCloture'), (4, 'Django-Model:VisiteSiteTouristique'), (17, 'Django-Model:VehiculeProprietaireDuplicata'), (18, 'Django-Model:BetailsPropriete'), (14, 'Django-Model:BaseActiviteDuplicata'), (5, 'Django-Model:AllocationEspacePublique'), (15, 'Django-Model:FoncierParcelleDuplicata'), (12, 'Django-Model:VehiculeActivite')], null=True),
        ),
        migrations.AlterField(
            model_name='noteimposition',
            name='entity',
            field=models.IntegerField(choices=[(13, 'Django-Model:VehiculeProprietaire'), (3, 'Django-Model:ActiviteExceptionnel'), (11, 'Django-Model:VehiculeActivite'), (2, 'Django-Model:Marche'), (6, 'Django-Model:AllocationPanneauPublicitaire'), (9, 'Location batiments municipaux'), (10, 'Django-Model:FoncierParcelle'), (8, 'Django-Model:AllocationPlaceMarche'), (16, 'Django-Model:VehiculeActiviteDuplicata'), (1, 'Django-Model:Standard'), (7, 'Django-Model:PubliciteMurCloture'), (4, 'Django-Model:VisiteSiteTouristique'), (17, 'Django-Model:VehiculeProprietaireDuplicata'), (18, 'Django-Model:BetailsPropriete'), (14, 'Django-Model:BaseActiviteDuplicata'), (5, 'Django-Model:AllocationEspacePublique'), (15, 'Django-Model:FoncierParcelleDuplicata'), (12, 'Django-Model:VehiculeActivite')], null=True),
        ),
        migrations.AlterField(
            model_name='periode',
            name='element',
            field=models.IntegerField(choices=[(8, 'Août'), (1, 'Janvier'), (19, 'Année'), (12, 'Décembre'), (3, 'Mars'), (14, '2e Trimestre'), (15, '3e Trimestre'), (17, '1er Semestre'), (18, '2e Semestre'), (13, '1er Trimestre'), (11, 'Novembre'), (10, 'Octobre'), (5, 'Mai'), (6, 'Juin'), (2, 'Février'), (4, 'Avril'), (9, 'Septembre'), (16, '4e Timestre'), (7, 'Juillet')], verbose_name='Elements de période'),
        ),
        migrations.AlterField(
            model_name='periodetype',
            name='categorie',
            field=models.IntegerField(choices=[(3, 'Semestrielle'), (0, 'Autre'), (1, 'Mensuelle'), (2, 'Trimestrielle'), (4, 'Annuelle')], default=0, verbose_name='catégorie de périodes'),
        ),
    ]
