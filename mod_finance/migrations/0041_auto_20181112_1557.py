# Generated by Django 2.0.7 on 2018-11-12 13:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mod_finance', '0040_auto_20181107_1348'),
    ]

    operations = [
        migrations.AlterField(
            model_name='avisimposition',
            name='entity',
            field=models.IntegerField(choices=[(15, 'Django-Model:FoncierParcelleDuplicata'), (14, 'Django-Model:BaseActiviteDuplicata'), (16, 'Django-Model:VehiculeActiviteDuplicata'), (5, 'Django-Model:AllocationEspacePublique'), (2, 'Django-Model:Marche'), (4, 'Django-Model:VisiteSiteTouristique'), (3, 'Django-Model:ActiviteExceptionnel'), (12, 'Django-Model:VehiculeActivite'), (18, 'Django-Model:BetailsPropriete'), (10, 'Django-Model:FoncierParcelle'), (11, 'Django-Model:VehiculeActivite'), (1, 'Django-Model:Standard'), (9, 'Location batiments municipaux'), (6, 'Django-Model:AllocationPanneauPublicitaire'), (13, 'Django-Model:VehiculeProprietaire'), (8, 'Django-Model:AllocationPlaceMarche'), (17, 'Django-Model:VehiculeProprietaireDuplicata'), (7, 'Django-Model:PubliciteMurCloture')], null=True),
        ),
        migrations.AlterField(
            model_name='noteimposition',
            name='entity',
            field=models.IntegerField(choices=[(15, 'Django-Model:FoncierParcelleDuplicata'), (14, 'Django-Model:BaseActiviteDuplicata'), (16, 'Django-Model:VehiculeActiviteDuplicata'), (5, 'Django-Model:AllocationEspacePublique'), (2, 'Django-Model:Marche'), (4, 'Django-Model:VisiteSiteTouristique'), (3, 'Django-Model:ActiviteExceptionnel'), (12, 'Django-Model:VehiculeActivite'), (18, 'Django-Model:BetailsPropriete'), (10, 'Django-Model:FoncierParcelle'), (11, 'Django-Model:VehiculeActivite'), (1, 'Django-Model:Standard'), (9, 'Location batiments municipaux'), (6, 'Django-Model:AllocationPanneauPublicitaire'), (13, 'Django-Model:VehiculeProprietaire'), (8, 'Django-Model:AllocationPlaceMarche'), (17, 'Django-Model:VehiculeProprietaireDuplicata'), (7, 'Django-Model:PubliciteMurCloture')], null=True),
        ),
        migrations.AlterField(
            model_name='periode',
            name='element',
            field=models.IntegerField(choices=[(6, 'Juin'), (18, '2e Semestre'), (10, 'Octobre'), (14, '2e Trimestre'), (19, 'Année'), (8, 'Août'), (17, '1er Semestre'), (7, 'Juillet'), (9, 'Septembre'), (2, 'Février'), (1, 'Janvier'), (12, 'Décembre'), (13, '1er Trimestre'), (16, '4e Trimestre'), (3, 'Mars'), (5, 'Mai'), (4, 'Avril'), (15, '3e Trimestre'), (11, 'Novembre')], verbose_name='Elements de période'),
        ),
        migrations.AlterField(
            model_name='periodetype',
            name='categorie',
            field=models.IntegerField(choices=[(4, 'Annuelle'), (3, 'Semestrielle'), (1, 'Mensuelle'), (2, 'Trimestrielle'), (0, 'Autre')], default=0, verbose_name='catégorie de périodes'),
        ),
    ]
