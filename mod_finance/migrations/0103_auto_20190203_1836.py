# Generated by Django 2.0.7 on 2019-02-03 16:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mod_finance', '0102_auto_20190201_1633'),
    ]

    operations = [
        migrations.AlterField(
            model_name='avisimposition',
            name='entity',
            field=models.IntegerField(choices=[(10, 'Django-Model:FoncierParcelle'), (2, 'Django-Model:Marche'), (11, 'Django-Model:VehiculeActivite'), (15, 'Django-Model:FoncierParcelleDuplicata'), (16, 'Django-Model:VehiculeActiviteDuplicata'), (6, 'Django-Model:AllocationPanneauPublicitaire'), (9, 'Location batiments municipaux'), (4, 'Django-Model:VisiteSiteTouristique'), (12, 'Django-Model:VehiculeActivite'), (14, 'Django-Model:BaseActiviteDuplicata'), (13, 'Django-Model:VehiculeProprietaire'), (7, 'Django-Model:PubliciteMurCloture'), (17, 'Django-Model:VehiculeProprietaireDuplicata'), (5, 'Django-Model:AllocationEspacePublique'), (3, 'Django-Model:ActiviteExceptionnel'), (1, 'Django-Model:Standard'), (18, 'Django-Model:BetailsPropriete'), (8, 'Django-Model:AllocationPlaceMarche')], null=True),
        ),
        migrations.AlterField(
            model_name='noteimposition',
            name='entity',
            field=models.IntegerField(choices=[(10, 'Django-Model:FoncierParcelle'), (2, 'Django-Model:Marche'), (11, 'Django-Model:VehiculeActivite'), (15, 'Django-Model:FoncierParcelleDuplicata'), (16, 'Django-Model:VehiculeActiviteDuplicata'), (6, 'Django-Model:AllocationPanneauPublicitaire'), (9, 'Location batiments municipaux'), (4, 'Django-Model:VisiteSiteTouristique'), (12, 'Django-Model:VehiculeActivite'), (14, 'Django-Model:BaseActiviteDuplicata'), (13, 'Django-Model:VehiculeProprietaire'), (7, 'Django-Model:PubliciteMurCloture'), (17, 'Django-Model:VehiculeProprietaireDuplicata'), (5, 'Django-Model:AllocationEspacePublique'), (3, 'Django-Model:ActiviteExceptionnel'), (1, 'Django-Model:Standard'), (18, 'Django-Model:BetailsPropriete'), (8, 'Django-Model:AllocationPlaceMarche')], null=True),
        ),
        migrations.AlterField(
            model_name='periode',
            name='element',
            field=models.IntegerField(choices=[(12, 'Décembre'), (14, '2e Trimestre'), (18, '2e Semestre'), (5, 'Mai'), (7, 'Juillet'), (2, 'Février'), (10, 'Octobre'), (3, 'Mars'), (11, 'Novembre'), (15, '3e Trimestre'), (17, '1er Semestre'), (9, 'Septembre'), (4, 'Avril'), (19, 'Année'), (8, 'Août'), (6, 'Juin'), (1, 'Janvier'), (13, '1er Trimestre'), (16, '4e Trimestre')], verbose_name='Elements de période'),
        ),
        migrations.AlterField(
            model_name='periodetype',
            name='categorie',
            field=models.IntegerField(choices=[(4, 'Annuelle'), (0, 'Autre'), (2, 'Trimestrielle'), (3, 'Semestrielle'), (1, 'Mensuelle')], default=0, verbose_name='catégorie de périodes'),
        ),
    ]
