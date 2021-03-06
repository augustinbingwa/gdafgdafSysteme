# Generated by Django 2.0.7 on 2019-02-01 10:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mod_finance', '0100_auto_20190126_1257'),
    ]

    operations = [
        migrations.AlterField(
            model_name='avisimposition',
            name='entity',
            field=models.IntegerField(choices=[(2, 'Django-Model:Marche'), (4, 'Django-Model:VisiteSiteTouristique'), (1, 'Django-Model:Standard'), (9, 'Location batiments municipaux'), (7, 'Django-Model:PubliciteMurCloture'), (11, 'Django-Model:VehiculeActivite'), (8, 'Django-Model:AllocationPlaceMarche'), (17, 'Django-Model:VehiculeProprietaireDuplicata'), (10, 'Django-Model:FoncierParcelle'), (3, 'Django-Model:ActiviteExceptionnel'), (13, 'Django-Model:VehiculeProprietaire'), (18, 'Django-Model:BetailsPropriete'), (16, 'Django-Model:VehiculeActiviteDuplicata'), (5, 'Django-Model:AllocationEspacePublique'), (12, 'Django-Model:VehiculeActivite'), (6, 'Django-Model:AllocationPanneauPublicitaire'), (15, 'Django-Model:FoncierParcelleDuplicata'), (14, 'Django-Model:BaseActiviteDuplicata')], null=True),
        ),
        migrations.AlterField(
            model_name='noteimposition',
            name='entity',
            field=models.IntegerField(choices=[(2, 'Django-Model:Marche'), (4, 'Django-Model:VisiteSiteTouristique'), (1, 'Django-Model:Standard'), (9, 'Location batiments municipaux'), (7, 'Django-Model:PubliciteMurCloture'), (11, 'Django-Model:VehiculeActivite'), (8, 'Django-Model:AllocationPlaceMarche'), (17, 'Django-Model:VehiculeProprietaireDuplicata'), (10, 'Django-Model:FoncierParcelle'), (3, 'Django-Model:ActiviteExceptionnel'), (13, 'Django-Model:VehiculeProprietaire'), (18, 'Django-Model:BetailsPropriete'), (16, 'Django-Model:VehiculeActiviteDuplicata'), (5, 'Django-Model:AllocationEspacePublique'), (12, 'Django-Model:VehiculeActivite'), (6, 'Django-Model:AllocationPanneauPublicitaire'), (15, 'Django-Model:FoncierParcelleDuplicata'), (14, 'Django-Model:BaseActiviteDuplicata')], null=True),
        ),
        migrations.AlterField(
            model_name='periode',
            name='element',
            field=models.IntegerField(choices=[(14, '2e Trimestre'), (15, '3e Trimestre'), (10, 'Octobre'), (11, 'Novembre'), (16, '4e Trimestre'), (9, 'Septembre'), (4, 'Avril'), (19, 'Ann??e'), (8, 'Ao??t'), (5, 'Mai'), (1, 'Janvier'), (6, 'Juin'), (3, 'Mars'), (12, 'D??cembre'), (18, '2e Semestre'), (2, 'F??vrier'), (17, '1er Semestre'), (7, 'Juillet'), (13, '1er Trimestre')], verbose_name='Elements de p??riode'),
        ),
        migrations.AlterField(
            model_name='periodetype',
            name='categorie',
            field=models.IntegerField(choices=[(3, 'Semestrielle'), (0, 'Autre'), (1, 'Mensuelle'), (2, 'Trimestrielle'), (4, 'Annuelle')], default=0, verbose_name='cat??gorie de p??riodes'),
        ),
    ]
