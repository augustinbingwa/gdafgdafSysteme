# Generated by Django 2.0.7 on 2019-02-13 08:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mod_finance', '0104_auto_20190203_1940'),
    ]

    operations = [
        migrations.AlterField(
            model_name='avisimposition',
            name='entity',
            field=models.IntegerField(choices=[(18, 'Django-Model:BetailsPropriete'), (5, 'Django-Model:AllocationEspacePublique'), (3, 'Django-Model:ActiviteExceptionnel'), (6, 'Django-Model:AllocationPanneauPublicitaire'), (12, 'Django-Model:VehiculeActivite'), (13, 'Django-Model:VehiculeProprietaire'), (10, 'Django-Model:FoncierParcelle'), (2, 'Django-Model:Marche'), (9, 'Location batiments municipaux'), (17, 'Django-Model:VehiculeProprietaireDuplicata'), (7, 'Django-Model:PubliciteMurCloture'), (11, 'Django-Model:VehiculeActivite'), (14, 'Django-Model:BaseActiviteDuplicata'), (4, 'Django-Model:VisiteSiteTouristique'), (15, 'Django-Model:FoncierParcelleDuplicata'), (8, 'Django-Model:AllocationPlaceMarche'), (16, 'Django-Model:VehiculeActiviteDuplicata'), (1, 'Django-Model:Standard')], null=True),
        ),
        migrations.AlterField(
            model_name='noteimposition',
            name='entity',
            field=models.IntegerField(choices=[(18, 'Django-Model:BetailsPropriete'), (5, 'Django-Model:AllocationEspacePublique'), (3, 'Django-Model:ActiviteExceptionnel'), (6, 'Django-Model:AllocationPanneauPublicitaire'), (12, 'Django-Model:VehiculeActivite'), (13, 'Django-Model:VehiculeProprietaire'), (10, 'Django-Model:FoncierParcelle'), (2, 'Django-Model:Marche'), (9, 'Location batiments municipaux'), (17, 'Django-Model:VehiculeProprietaireDuplicata'), (7, 'Django-Model:PubliciteMurCloture'), (11, 'Django-Model:VehiculeActivite'), (14, 'Django-Model:BaseActiviteDuplicata'), (4, 'Django-Model:VisiteSiteTouristique'), (15, 'Django-Model:FoncierParcelleDuplicata'), (8, 'Django-Model:AllocationPlaceMarche'), (16, 'Django-Model:VehiculeActiviteDuplicata'), (1, 'Django-Model:Standard')], null=True),
        ),
        migrations.AlterField(
            model_name='periode',
            name='element',
            field=models.IntegerField(choices=[(19, 'Ann??e'), (2, 'F??vrier'), (10, 'Octobre'), (18, '2e Semestre'), (15, '3e Trimestre'), (5, 'Mai'), (14, '2e Trimestre'), (1, 'Janvier'), (16, '4e Trimestre'), (8, 'Ao??t'), (4, 'Avril'), (7, 'Juillet'), (12, 'D??cembre'), (6, 'Juin'), (11, 'Novembre'), (17, '1er Semestre'), (13, '1er Trimestre'), (3, 'Mars'), (9, 'Septembre')], verbose_name='Elements de p??riode'),
        ),
        migrations.AlterField(
            model_name='periodetype',
            name='categorie',
            field=models.IntegerField(choices=[(0, 'Autre'), (1, 'Mensuelle'), (3, 'Semestrielle'), (2, 'Trimestrielle'), (4, 'Annuelle')], default=0, verbose_name='cat??gorie de p??riodes'),
        ),
    ]
