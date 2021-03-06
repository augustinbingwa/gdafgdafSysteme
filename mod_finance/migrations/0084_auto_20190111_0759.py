# Generated by Django 2.0.7 on 2019-01-11 05:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mod_finance', '0083_auto_20190110_2220'),
    ]

    operations = [
        migrations.AlterField(
            model_name='avisimposition',
            name='entity',
            field=models.IntegerField(choices=[(11, 'Django-Model:VehiculeActivite'), (1, 'Django-Model:Standard'), (5, 'Django-Model:AllocationEspacePublique'), (18, 'Django-Model:BetailsPropriete'), (2, 'Django-Model:Marche'), (15, 'Django-Model:FoncierParcelleDuplicata'), (13, 'Django-Model:VehiculeProprietaire'), (7, 'Django-Model:PubliciteMurCloture'), (9, 'Location batiments municipaux'), (16, 'Django-Model:VehiculeActiviteDuplicata'), (17, 'Django-Model:VehiculeProprietaireDuplicata'), (8, 'Django-Model:AllocationPlaceMarche'), (3, 'Django-Model:ActiviteExceptionnel'), (4, 'Django-Model:VisiteSiteTouristique'), (10, 'Django-Model:FoncierParcelle'), (12, 'Django-Model:VehiculeActivite'), (14, 'Django-Model:BaseActiviteDuplicata'), (6, 'Django-Model:AllocationPanneauPublicitaire')], null=True),
        ),
        migrations.AlterField(
            model_name='noteimposition',
            name='entity',
            field=models.IntegerField(choices=[(11, 'Django-Model:VehiculeActivite'), (1, 'Django-Model:Standard'), (5, 'Django-Model:AllocationEspacePublique'), (18, 'Django-Model:BetailsPropriete'), (2, 'Django-Model:Marche'), (15, 'Django-Model:FoncierParcelleDuplicata'), (13, 'Django-Model:VehiculeProprietaire'), (7, 'Django-Model:PubliciteMurCloture'), (9, 'Location batiments municipaux'), (16, 'Django-Model:VehiculeActiviteDuplicata'), (17, 'Django-Model:VehiculeProprietaireDuplicata'), (8, 'Django-Model:AllocationPlaceMarche'), (3, 'Django-Model:ActiviteExceptionnel'), (4, 'Django-Model:VisiteSiteTouristique'), (10, 'Django-Model:FoncierParcelle'), (12, 'Django-Model:VehiculeActivite'), (14, 'Django-Model:BaseActiviteDuplicata'), (6, 'Django-Model:AllocationPanneauPublicitaire')], null=True),
        ),
        migrations.AlterField(
            model_name='periode',
            name='element',
            field=models.IntegerField(choices=[(10, 'Octobre'), (5, 'Mai'), (7, 'Juillet'), (8, 'Ao??t'), (12, 'D??cembre'), (1, 'Janvier'), (13, '1er Trimestre'), (15, '3e Trimestre'), (17, '1er Semestre'), (3, 'Mars'), (9, 'Septembre'), (11, 'Novembre'), (14, '2e Trimestre'), (18, '2e Semestre'), (19, 'Ann??e'), (2, 'F??vrier'), (6, 'Juin'), (4, 'Avril'), (16, '4e Trimestre')], verbose_name='Elements de p??riode'),
        ),
        migrations.AlterField(
            model_name='periodetype',
            name='categorie',
            field=models.IntegerField(choices=[(4, 'Annuelle'), (0, 'Autre'), (1, 'Mensuelle'), (3, 'Semestrielle'), (2, 'Trimestrielle')], default=0, verbose_name='cat??gorie de p??riodes'),
        ),
    ]
