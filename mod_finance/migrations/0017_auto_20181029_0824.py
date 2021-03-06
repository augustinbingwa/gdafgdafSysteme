# Generated by Django 2.0.7 on 2018-10-29 06:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mod_finance', '0016_auto_20181029_0824'),
    ]

    operations = [
        migrations.AlterField(
            model_name='avisimposition',
            name='entity',
            field=models.IntegerField(choices=[(1, 'Django-Model:Standard'), (6, 'Django-Model:AllocationPanneauPublicitaire'), (8, 'Django-Model:AllocationPlaceMarche'), (11, 'Django-Model:VehiculeActivite'), (2, 'Django-Model:Marche'), (7, 'Django-Model:PubliciteMurCloture'), (13, 'Django-Model:VehiculeProprietaire'), (14, 'Django-Model:BaseActiviteDuplicata'), (15, 'Django-Model:FoncierParcelleDuplicata'), (17, 'Django-Model:VehiculeProprietaireDuplicata'), (18, 'Django-Model:BetailsPropriete'), (10, 'Django-Model:FoncierParcelle'), (12, 'Django-Model:VehiculeActivite'), (4, 'Django-Model:VisiteSiteTouristique'), (3, 'Django-Model:ActiviteExceptionnel'), (9, 'Location batiments municipaux'), (5, 'Django-Model:AllocationEspacePublique'), (16, 'Django-Model:VehiculeActiviteDuplicata')], null=True),
        ),
        migrations.AlterField(
            model_name='noteimposition',
            name='entity',
            field=models.IntegerField(choices=[(1, 'Django-Model:Standard'), (6, 'Django-Model:AllocationPanneauPublicitaire'), (8, 'Django-Model:AllocationPlaceMarche'), (11, 'Django-Model:VehiculeActivite'), (2, 'Django-Model:Marche'), (7, 'Django-Model:PubliciteMurCloture'), (13, 'Django-Model:VehiculeProprietaire'), (14, 'Django-Model:BaseActiviteDuplicata'), (15, 'Django-Model:FoncierParcelleDuplicata'), (17, 'Django-Model:VehiculeProprietaireDuplicata'), (18, 'Django-Model:BetailsPropriete'), (10, 'Django-Model:FoncierParcelle'), (12, 'Django-Model:VehiculeActivite'), (4, 'Django-Model:VisiteSiteTouristique'), (3, 'Django-Model:ActiviteExceptionnel'), (9, 'Location batiments municipaux'), (5, 'Django-Model:AllocationEspacePublique'), (16, 'Django-Model:VehiculeActiviteDuplicata')], null=True),
        ),
        migrations.AlterField(
            model_name='periode',
            name='element',
            field=models.IntegerField(choices=[(8, 'Ao??t'), (10, 'Octobre'), (2, 'F??vrier'), (5, 'Mai'), (7, 'Juillet'), (12, 'D??cembre'), (15, '3e Trimestre'), (19, 'Ann??e'), (13, '1er Trimestre'), (9, 'Septembre'), (6, 'Juin'), (16, '4e Timestre'), (3, 'Mars'), (14, '2e Trimestre'), (11, 'Novembre'), (4, 'Avril'), (1, 'Janvier'), (18, '2e Semestre'), (17, '1er Semestre')], verbose_name='Elements de p??riode'),
        ),
        migrations.AlterField(
            model_name='periodetype',
            name='categorie',
            field=models.IntegerField(choices=[(3, 'Semestrielle'), (1, 'Mensuelle'), (0, 'Autre'), (4, 'Annuelle'), (2, 'Trimestrielle')], default=0, verbose_name='cat??gorie de p??riodes'),
        ),
    ]
