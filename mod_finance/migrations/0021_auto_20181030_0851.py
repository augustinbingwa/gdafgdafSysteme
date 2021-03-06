# Generated by Django 2.0.7 on 2018-10-30 06:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mod_finance', '0020_auto_20181029_2346'),
    ]

    operations = [
        migrations.AlterField(
            model_name='avisimposition',
            name='entity',
            field=models.IntegerField(choices=[(18, 'Django-Model:BetailsPropriete'), (1, 'Django-Model:Standard'), (10, 'Django-Model:FoncierParcelle'), (9, 'Location batiments municipaux'), (12, 'Django-Model:VehiculeActivite'), (17, 'Django-Model:VehiculeProprietaireDuplicata'), (3, 'Django-Model:ActiviteExceptionnel'), (8, 'Django-Model:AllocationPlaceMarche'), (16, 'Django-Model:VehiculeActiviteDuplicata'), (5, 'Django-Model:AllocationEspacePublique'), (15, 'Django-Model:FoncierParcelleDuplicata'), (7, 'Django-Model:PubliciteMurCloture'), (11, 'Django-Model:VehiculeActivite'), (14, 'Django-Model:BaseActiviteDuplicata'), (6, 'Django-Model:AllocationPanneauPublicitaire'), (13, 'Django-Model:VehiculeProprietaire'), (2, 'Django-Model:Marche'), (4, 'Django-Model:VisiteSiteTouristique')], null=True),
        ),
        migrations.AlterField(
            model_name='noteimposition',
            name='entity',
            field=models.IntegerField(choices=[(18, 'Django-Model:BetailsPropriete'), (1, 'Django-Model:Standard'), (10, 'Django-Model:FoncierParcelle'), (9, 'Location batiments municipaux'), (12, 'Django-Model:VehiculeActivite'), (17, 'Django-Model:VehiculeProprietaireDuplicata'), (3, 'Django-Model:ActiviteExceptionnel'), (8, 'Django-Model:AllocationPlaceMarche'), (16, 'Django-Model:VehiculeActiviteDuplicata'), (5, 'Django-Model:AllocationEspacePublique'), (15, 'Django-Model:FoncierParcelleDuplicata'), (7, 'Django-Model:PubliciteMurCloture'), (11, 'Django-Model:VehiculeActivite'), (14, 'Django-Model:BaseActiviteDuplicata'), (6, 'Django-Model:AllocationPanneauPublicitaire'), (13, 'Django-Model:VehiculeProprietaire'), (2, 'Django-Model:Marche'), (4, 'Django-Model:VisiteSiteTouristique')], null=True),
        ),
        migrations.AlterField(
            model_name='periode',
            name='element',
            field=models.IntegerField(choices=[(14, '2e Trimestre'), (15, '3e Trimestre'), (18, '2e Semestre'), (19, 'Ann??e'), (6, 'Juin'), (5, 'Mai'), (13, '1er Trimestre'), (2, 'F??vrier'), (16, '4e Timestre'), (9, 'Septembre'), (17, '1er Semestre'), (4, 'Avril'), (8, 'Ao??t'), (1, 'Janvier'), (12, 'D??cembre'), (11, 'Novembre'), (3, 'Mars'), (7, 'Juillet'), (10, 'Octobre')], verbose_name='Elements de p??riode'),
        ),
        migrations.AlterField(
            model_name='periodetype',
            name='categorie',
            field=models.IntegerField(choices=[(4, 'Annuelle'), (3, 'Semestrielle'), (0, 'Autre'), (1, 'Mensuelle'), (2, 'Trimestrielle')], default=0, verbose_name='cat??gorie de p??riodes'),
        ),
    ]
