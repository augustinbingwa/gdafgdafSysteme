# Generated by Django 2.0.7 on 2019-02-24 13:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mod_finance', '0110_auto_20190224_1501'),
    ]

    operations = [
        migrations.AlterField(
            model_name='avisimposition',
            name='entity',
            field=models.IntegerField(choices=[(14, 'Django-Model:BaseActiviteDuplicata'), (3, 'Django-Model:ActiviteExceptionnel'), (10, 'Django-Model:FoncierParcelle'), (12, 'Django-Model:VehiculeActivite'), (6, 'Django-Model:AllocationPanneauPublicitaire'), (4, 'Django-Model:VisiteSiteTouristique'), (2, 'Django-Model:Marche'), (7, 'Django-Model:PubliciteMurCloture'), (17, 'Django-Model:VehiculeProprietaireDuplicata'), (1, 'Django-Model:Standard'), (18, 'Django-Model:BetailsPropriete'), (9, 'Location batiments municipaux'), (11, 'Django-Model:VehiculeActivite'), (8, 'Django-Model:AllocationPlaceMarche'), (13, 'Django-Model:VehiculeProprietaire'), (15, 'Django-Model:FoncierParcelleDuplicata'), (16, 'Django-Model:VehiculeActiviteDuplicata'), (5, 'Django-Model:AllocationEspacePublique')], null=True),
        ),
        migrations.AlterField(
            model_name='noteimposition',
            name='entity',
            field=models.IntegerField(choices=[(14, 'Django-Model:BaseActiviteDuplicata'), (3, 'Django-Model:ActiviteExceptionnel'), (10, 'Django-Model:FoncierParcelle'), (12, 'Django-Model:VehiculeActivite'), (6, 'Django-Model:AllocationPanneauPublicitaire'), (4, 'Django-Model:VisiteSiteTouristique'), (2, 'Django-Model:Marche'), (7, 'Django-Model:PubliciteMurCloture'), (17, 'Django-Model:VehiculeProprietaireDuplicata'), (1, 'Django-Model:Standard'), (18, 'Django-Model:BetailsPropriete'), (9, 'Location batiments municipaux'), (11, 'Django-Model:VehiculeActivite'), (8, 'Django-Model:AllocationPlaceMarche'), (13, 'Django-Model:VehiculeProprietaire'), (15, 'Django-Model:FoncierParcelleDuplicata'), (16, 'Django-Model:VehiculeActiviteDuplicata'), (5, 'Django-Model:AllocationEspacePublique')], null=True),
        ),
        migrations.AlterField(
            model_name='periode',
            name='element',
            field=models.IntegerField(choices=[(19, 'Année'), (18, '2e Semestre'), (7, 'Juillet'), (12, 'Décembre'), (17, '1er Semestre'), (2, 'Février'), (13, '1er Trimestre'), (5, 'Mai'), (4, 'Avril'), (9, 'Septembre'), (14, '2e Trimestre'), (1, 'Janvier'), (8, 'Août'), (11, 'Novembre'), (3, 'Mars'), (16, '4e Trimestre'), (15, '3e Trimestre'), (6, 'Juin'), (10, 'Octobre')], verbose_name='Elements de période'),
        ),
        migrations.AlterField(
            model_name='periodetype',
            name='categorie',
            field=models.IntegerField(choices=[(2, 'Trimestrielle'), (3, 'Semestrielle'), (4, 'Annuelle'), (0, 'Autre'), (1, 'Mensuelle')], default=0, verbose_name='catégorie de périodes'),
        ),
    ]