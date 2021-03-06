# Generated by Django 2.0.7 on 2018-10-31 16:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mod_finance', '0024_auto_20181031_1731'),
    ]

    operations = [
        migrations.AlterField(
            model_name='avisimposition',
            name='entity',
            field=models.IntegerField(choices=[(5, 'Django-Model:AllocationEspacePublique'), (9, 'Location batiments municipaux'), (18, 'Django-Model:BetailsPropriete'), (16, 'Django-Model:VehiculeActiviteDuplicata'), (15, 'Django-Model:FoncierParcelleDuplicata'), (8, 'Django-Model:AllocationPlaceMarche'), (10, 'Django-Model:FoncierParcelle'), (17, 'Django-Model:VehiculeProprietaireDuplicata'), (1, 'Django-Model:Standard'), (13, 'Django-Model:VehiculeProprietaire'), (4, 'Django-Model:VisiteSiteTouristique'), (11, 'Django-Model:VehiculeActivite'), (12, 'Django-Model:VehiculeActivite'), (6, 'Django-Model:AllocationPanneauPublicitaire'), (3, 'Django-Model:ActiviteExceptionnel'), (14, 'Django-Model:BaseActiviteDuplicata'), (7, 'Django-Model:PubliciteMurCloture'), (2, 'Django-Model:Marche')], null=True),
        ),
        migrations.AlterField(
            model_name='noteimposition',
            name='entity',
            field=models.IntegerField(choices=[(5, 'Django-Model:AllocationEspacePublique'), (9, 'Location batiments municipaux'), (18, 'Django-Model:BetailsPropriete'), (16, 'Django-Model:VehiculeActiviteDuplicata'), (15, 'Django-Model:FoncierParcelleDuplicata'), (8, 'Django-Model:AllocationPlaceMarche'), (10, 'Django-Model:FoncierParcelle'), (17, 'Django-Model:VehiculeProprietaireDuplicata'), (1, 'Django-Model:Standard'), (13, 'Django-Model:VehiculeProprietaire'), (4, 'Django-Model:VisiteSiteTouristique'), (11, 'Django-Model:VehiculeActivite'), (12, 'Django-Model:VehiculeActivite'), (6, 'Django-Model:AllocationPanneauPublicitaire'), (3, 'Django-Model:ActiviteExceptionnel'), (14, 'Django-Model:BaseActiviteDuplicata'), (7, 'Django-Model:PubliciteMurCloture'), (2, 'Django-Model:Marche')], null=True),
        ),
        migrations.AlterField(
            model_name='periode',
            name='element',
            field=models.IntegerField(choices=[(18, '2e Semestre'), (9, 'Septembre'), (10, 'Octobre'), (15, '3e Trimestre'), (4, 'Avril'), (6, 'Juin'), (17, '1er Semestre'), (8, 'Ao??t'), (19, 'Ann??e'), (5, 'Mai'), (12, 'D??cembre'), (1, 'Janvier'), (16, '4e Timestre'), (7, 'Juillet'), (3, 'Mars'), (11, 'Novembre'), (2, 'F??vrier'), (13, '1er Trimestre'), (14, '2e Trimestre')], verbose_name='Elements de p??riode'),
        ),
        migrations.AlterField(
            model_name='periodetype',
            name='categorie',
            field=models.IntegerField(choices=[(1, 'Mensuelle'), (2, 'Trimestrielle'), (0, 'Autre'), (4, 'Annuelle'), (3, 'Semestrielle')], default=0, verbose_name='cat??gorie de p??riodes'),
        ),
    ]
