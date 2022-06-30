# Generated by Django 2.0.7 on 2018-12-09 18:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mod_finance', '0061_auto_20181208_1237'),
    ]

    operations = [
        migrations.AlterField(
            model_name='avisimposition',
            name='entity',
            field=models.IntegerField(choices=[(14, 'Django-Model:BaseActiviteDuplicata'), (15, 'Django-Model:FoncierParcelleDuplicata'), (16, 'Django-Model:VehiculeActiviteDuplicata'), (18, 'Django-Model:BetailsPropriete'), (13, 'Django-Model:VehiculeProprietaire'), (10, 'Django-Model:FoncierParcelle'), (8, 'Django-Model:AllocationPlaceMarche'), (7, 'Django-Model:PubliciteMurCloture'), (4, 'Django-Model:VisiteSiteTouristique'), (5, 'Django-Model:AllocationEspacePublique'), (11, 'Django-Model:VehiculeActivite'), (2, 'Django-Model:Marche'), (17, 'Django-Model:VehiculeProprietaireDuplicata'), (1, 'Django-Model:Standard'), (9, 'Location batiments municipaux'), (12, 'Django-Model:VehiculeActivite'), (3, 'Django-Model:ActiviteExceptionnel'), (6, 'Django-Model:AllocationPanneauPublicitaire')], null=True),
        ),
        migrations.AlterField(
            model_name='noteimposition',
            name='entity',
            field=models.IntegerField(choices=[(14, 'Django-Model:BaseActiviteDuplicata'), (15, 'Django-Model:FoncierParcelleDuplicata'), (16, 'Django-Model:VehiculeActiviteDuplicata'), (18, 'Django-Model:BetailsPropriete'), (13, 'Django-Model:VehiculeProprietaire'), (10, 'Django-Model:FoncierParcelle'), (8, 'Django-Model:AllocationPlaceMarche'), (7, 'Django-Model:PubliciteMurCloture'), (4, 'Django-Model:VisiteSiteTouristique'), (5, 'Django-Model:AllocationEspacePublique'), (11, 'Django-Model:VehiculeActivite'), (2, 'Django-Model:Marche'), (17, 'Django-Model:VehiculeProprietaireDuplicata'), (1, 'Django-Model:Standard'), (9, 'Location batiments municipaux'), (12, 'Django-Model:VehiculeActivite'), (3, 'Django-Model:ActiviteExceptionnel'), (6, 'Django-Model:AllocationPanneauPublicitaire')], null=True),
        ),
        migrations.AlterField(
            model_name='periode',
            name='element',
            field=models.IntegerField(choices=[(15, '3e Trimestre'), (13, '1er Trimestre'), (18, '2e Semestre'), (4, 'Avril'), (10, 'Octobre'), (5, 'Mai'), (8, 'Août'), (3, 'Mars'), (6, 'Juin'), (9, 'Septembre'), (11, 'Novembre'), (14, '2e Trimestre'), (16, '4e Trimestre'), (17, '1er Semestre'), (19, 'Année'), (1, 'Janvier'), (2, 'Février'), (12, 'Décembre'), (7, 'Juillet')], verbose_name='Elements de période'),
        ),
        migrations.AlterField(
            model_name='periodetype',
            name='categorie',
            field=models.IntegerField(choices=[(0, 'Autre'), (3, 'Semestrielle'), (2, 'Trimestrielle'), (4, 'Annuelle'), (1, 'Mensuelle')], default=0, verbose_name='catégorie de périodes'),
        ),
    ]
