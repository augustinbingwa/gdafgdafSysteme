# Generated by Django 2.0.7 on 2018-12-07 09:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mod_finance', '0057_auto_20181207_1128'),
    ]

    operations = [
        migrations.AlterField(
            model_name='avisimposition',
            name='entity',
            field=models.IntegerField(choices=[(3, 'Django-Model:ActiviteExceptionnel'), (17, 'Django-Model:VehiculeProprietaireDuplicata'), (5, 'Django-Model:AllocationEspacePublique'), (10, 'Django-Model:FoncierParcelle'), (12, 'Django-Model:VehiculeActivite'), (6, 'Django-Model:AllocationPanneauPublicitaire'), (8, 'Django-Model:AllocationPlaceMarche'), (18, 'Django-Model:BetailsPropriete'), (15, 'Django-Model:FoncierParcelleDuplicata'), (9, 'Location batiments municipaux'), (7, 'Django-Model:PubliciteMurCloture'), (4, 'Django-Model:VisiteSiteTouristique'), (11, 'Django-Model:VehiculeActivite'), (1, 'Django-Model:Standard'), (14, 'Django-Model:BaseActiviteDuplicata'), (16, 'Django-Model:VehiculeActiviteDuplicata'), (13, 'Django-Model:VehiculeProprietaire'), (2, 'Django-Model:Marche')], null=True),
        ),
        migrations.AlterField(
            model_name='noteimposition',
            name='entity',
            field=models.IntegerField(choices=[(3, 'Django-Model:ActiviteExceptionnel'), (17, 'Django-Model:VehiculeProprietaireDuplicata'), (5, 'Django-Model:AllocationEspacePublique'), (10, 'Django-Model:FoncierParcelle'), (12, 'Django-Model:VehiculeActivite'), (6, 'Django-Model:AllocationPanneauPublicitaire'), (8, 'Django-Model:AllocationPlaceMarche'), (18, 'Django-Model:BetailsPropriete'), (15, 'Django-Model:FoncierParcelleDuplicata'), (9, 'Location batiments municipaux'), (7, 'Django-Model:PubliciteMurCloture'), (4, 'Django-Model:VisiteSiteTouristique'), (11, 'Django-Model:VehiculeActivite'), (1, 'Django-Model:Standard'), (14, 'Django-Model:BaseActiviteDuplicata'), (16, 'Django-Model:VehiculeActiviteDuplicata'), (13, 'Django-Model:VehiculeProprietaire'), (2, 'Django-Model:Marche')], null=True),
        ),
        migrations.AlterField(
            model_name='periode',
            name='element',
            field=models.IntegerField(choices=[(10, 'Octobre'), (1, 'Janvier'), (16, '4e Trimestre'), (6, 'Juin'), (2, 'Février'), (4, 'Avril'), (3, 'Mars'), (8, 'Août'), (18, '2e Semestre'), (17, '1er Semestre'), (13, '1er Trimestre'), (15, '3e Trimestre'), (7, 'Juillet'), (11, 'Novembre'), (5, 'Mai'), (9, 'Septembre'), (12, 'Décembre'), (14, '2e Trimestre'), (19, 'Année')], verbose_name='Elements de période'),
        ),
        migrations.AlterField(
            model_name='periodetype',
            name='categorie',
            field=models.IntegerField(choices=[(3, 'Semestrielle'), (2, 'Trimestrielle'), (1, 'Mensuelle'), (4, 'Annuelle'), (0, 'Autre')], default=0, verbose_name='catégorie de périodes'),
        ),
    ]