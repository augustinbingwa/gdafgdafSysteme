# Generated by Django 2.0.7 on 2018-11-15 15:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mod_finance', '0044_auto_20181115_1438'),
    ]

    operations = [
        migrations.AlterField(
            model_name='avisimposition',
            name='entity',
            field=models.IntegerField(choices=[(1, 'Django-Model:Standard'), (2, 'Django-Model:Marche'), (5, 'Django-Model:AllocationEspacePublique'), (9, 'Location batiments municipaux'), (10, 'Django-Model:FoncierParcelle'), (4, 'Django-Model:VisiteSiteTouristique'), (11, 'Django-Model:VehiculeActivite'), (13, 'Django-Model:VehiculeProprietaire'), (15, 'Django-Model:FoncierParcelleDuplicata'), (16, 'Django-Model:VehiculeActiviteDuplicata'), (18, 'Django-Model:BetailsPropriete'), (7, 'Django-Model:PubliciteMurCloture'), (6, 'Django-Model:AllocationPanneauPublicitaire'), (17, 'Django-Model:VehiculeProprietaireDuplicata'), (3, 'Django-Model:ActiviteExceptionnel'), (12, 'Django-Model:VehiculeActivite'), (8, 'Django-Model:AllocationPlaceMarche'), (14, 'Django-Model:BaseActiviteDuplicata')], null=True),
        ),
        migrations.AlterField(
            model_name='noteimposition',
            name='entity',
            field=models.IntegerField(choices=[(1, 'Django-Model:Standard'), (2, 'Django-Model:Marche'), (5, 'Django-Model:AllocationEspacePublique'), (9, 'Location batiments municipaux'), (10, 'Django-Model:FoncierParcelle'), (4, 'Django-Model:VisiteSiteTouristique'), (11, 'Django-Model:VehiculeActivite'), (13, 'Django-Model:VehiculeProprietaire'), (15, 'Django-Model:FoncierParcelleDuplicata'), (16, 'Django-Model:VehiculeActiviteDuplicata'), (18, 'Django-Model:BetailsPropriete'), (7, 'Django-Model:PubliciteMurCloture'), (6, 'Django-Model:AllocationPanneauPublicitaire'), (17, 'Django-Model:VehiculeProprietaireDuplicata'), (3, 'Django-Model:ActiviteExceptionnel'), (12, 'Django-Model:VehiculeActivite'), (8, 'Django-Model:AllocationPlaceMarche'), (14, 'Django-Model:BaseActiviteDuplicata')], null=True),
        ),
        migrations.AlterField(
            model_name='periode',
            name='element',
            field=models.IntegerField(choices=[(5, 'Mai'), (3, 'Mars'), (6, 'Juin'), (12, 'D??cembre'), (16, '4e Trimestre'), (18, '2e Semestre'), (2, 'F??vrier'), (13, '1er Trimestre'), (9, 'Septembre'), (4, 'Avril'), (8, 'Ao??t'), (15, '3e Trimestre'), (19, 'Ann??e'), (7, 'Juillet'), (11, 'Novembre'), (10, 'Octobre'), (14, '2e Trimestre'), (17, '1er Semestre'), (1, 'Janvier')], verbose_name='Elements de p??riode'),
        ),
        migrations.AlterField(
            model_name='periodetype',
            name='categorie',
            field=models.IntegerField(choices=[(3, 'Semestrielle'), (4, 'Annuelle'), (1, 'Mensuelle'), (2, 'Trimestrielle'), (0, 'Autre')], default=0, verbose_name='cat??gorie de p??riodes'),
        ),
    ]
