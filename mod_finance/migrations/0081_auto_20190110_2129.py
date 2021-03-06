# Generated by Django 2.0.7 on 2019-01-10 19:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mod_finance', '0080_auto_20190110_2125'),
    ]

    operations = [
        migrations.AlterField(
            model_name='avisimposition',
            name='entity',
            field=models.IntegerField(choices=[(17, 'Django-Model:VehiculeProprietaireDuplicata'), (3, 'Django-Model:ActiviteExceptionnel'), (4, 'Django-Model:VisiteSiteTouristique'), (5, 'Django-Model:AllocationEspacePublique'), (10, 'Django-Model:FoncierParcelle'), (11, 'Django-Model:VehiculeActivite'), (15, 'Django-Model:FoncierParcelleDuplicata'), (16, 'Django-Model:VehiculeActiviteDuplicata'), (14, 'Django-Model:BaseActiviteDuplicata'), (2, 'Django-Model:Marche'), (1, 'Django-Model:Standard'), (13, 'Django-Model:VehiculeProprietaire'), (7, 'Django-Model:PubliciteMurCloture'), (18, 'Django-Model:BetailsPropriete'), (12, 'Django-Model:VehiculeActivite'), (8, 'Django-Model:AllocationPlaceMarche'), (9, 'Location batiments municipaux'), (6, 'Django-Model:AllocationPanneauPublicitaire')], null=True),
        ),
        migrations.AlterField(
            model_name='noteimposition',
            name='entity',
            field=models.IntegerField(choices=[(17, 'Django-Model:VehiculeProprietaireDuplicata'), (3, 'Django-Model:ActiviteExceptionnel'), (4, 'Django-Model:VisiteSiteTouristique'), (5, 'Django-Model:AllocationEspacePublique'), (10, 'Django-Model:FoncierParcelle'), (11, 'Django-Model:VehiculeActivite'), (15, 'Django-Model:FoncierParcelleDuplicata'), (16, 'Django-Model:VehiculeActiviteDuplicata'), (14, 'Django-Model:BaseActiviteDuplicata'), (2, 'Django-Model:Marche'), (1, 'Django-Model:Standard'), (13, 'Django-Model:VehiculeProprietaire'), (7, 'Django-Model:PubliciteMurCloture'), (18, 'Django-Model:BetailsPropriete'), (12, 'Django-Model:VehiculeActivite'), (8, 'Django-Model:AllocationPlaceMarche'), (9, 'Location batiments municipaux'), (6, 'Django-Model:AllocationPanneauPublicitaire')], null=True),
        ),
        migrations.AlterField(
            model_name='periode',
            name='element',
            field=models.IntegerField(choices=[(10, 'Octobre'), (2, 'F??vrier'), (9, 'Septembre'), (4, 'Avril'), (13, '1er Trimestre'), (18, '2e Semestre'), (1, 'Janvier'), (3, 'Mars'), (12, 'D??cembre'), (7, 'Juillet'), (16, '4e Trimestre'), (17, '1er Semestre'), (14, '2e Trimestre'), (19, 'Ann??e'), (11, 'Novembre'), (8, 'Ao??t'), (6, 'Juin'), (5, 'Mai'), (15, '3e Trimestre')], verbose_name='Elements de p??riode'),
        ),
        migrations.AlterField(
            model_name='periodetype',
            name='categorie',
            field=models.IntegerField(choices=[(3, 'Semestrielle'), (0, 'Autre'), (1, 'Mensuelle'), (2, 'Trimestrielle'), (4, 'Annuelle')], default=0, verbose_name='cat??gorie de p??riodes'),
        ),
    ]
