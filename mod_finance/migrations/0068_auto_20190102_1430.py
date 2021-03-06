# Generated by Django 2.0.7 on 2019-01-02 12:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mod_finance', '0067_auto_20190102_0854'),
    ]

    operations = [
        migrations.AlterField(
            model_name='avisimposition',
            name='entity',
            field=models.IntegerField(choices=[(5, 'Django-Model:AllocationEspacePublique'), (1, 'Django-Model:Standard'), (4, 'Django-Model:VisiteSiteTouristique'), (6, 'Django-Model:AllocationPanneauPublicitaire'), (10, 'Django-Model:FoncierParcelle'), (14, 'Django-Model:BaseActiviteDuplicata'), (15, 'Django-Model:FoncierParcelleDuplicata'), (18, 'Django-Model:BetailsPropriete'), (12, 'Django-Model:VehiculeActivite'), (13, 'Django-Model:VehiculeProprietaire'), (9, 'Location batiments municipaux'), (7, 'Django-Model:PubliciteMurCloture'), (17, 'Django-Model:VehiculeProprietaireDuplicata'), (3, 'Django-Model:ActiviteExceptionnel'), (11, 'Django-Model:VehiculeActivite'), (2, 'Django-Model:Marche'), (16, 'Django-Model:VehiculeActiviteDuplicata'), (8, 'Django-Model:AllocationPlaceMarche')], null=True),
        ),
        migrations.AlterField(
            model_name='noteimposition',
            name='entity',
            field=models.IntegerField(choices=[(5, 'Django-Model:AllocationEspacePublique'), (1, 'Django-Model:Standard'), (4, 'Django-Model:VisiteSiteTouristique'), (6, 'Django-Model:AllocationPanneauPublicitaire'), (10, 'Django-Model:FoncierParcelle'), (14, 'Django-Model:BaseActiviteDuplicata'), (15, 'Django-Model:FoncierParcelleDuplicata'), (18, 'Django-Model:BetailsPropriete'), (12, 'Django-Model:VehiculeActivite'), (13, 'Django-Model:VehiculeProprietaire'), (9, 'Location batiments municipaux'), (7, 'Django-Model:PubliciteMurCloture'), (17, 'Django-Model:VehiculeProprietaireDuplicata'), (3, 'Django-Model:ActiviteExceptionnel'), (11, 'Django-Model:VehiculeActivite'), (2, 'Django-Model:Marche'), (16, 'Django-Model:VehiculeActiviteDuplicata'), (8, 'Django-Model:AllocationPlaceMarche')], null=True),
        ),
        migrations.AlterField(
            model_name='periode',
            name='element',
            field=models.IntegerField(choices=[(12, 'D??cembre'), (14, '2e Trimestre'), (8, 'Ao??t'), (16, '4e Trimestre'), (17, '1er Semestre'), (2, 'F??vrier'), (1, 'Janvier'), (9, 'Septembre'), (10, 'Octobre'), (4, 'Avril'), (13, '1er Trimestre'), (15, '3e Trimestre'), (18, '2e Semestre'), (6, 'Juin'), (3, 'Mars'), (19, 'Ann??e'), (5, 'Mai'), (11, 'Novembre'), (7, 'Juillet')], verbose_name='Elements de p??riode'),
        ),
        migrations.AlterField(
            model_name='periodetype',
            name='categorie',
            field=models.IntegerField(choices=[(0, 'Autre'), (2, 'Trimestrielle'), (4, 'Annuelle'), (3, 'Semestrielle'), (1, 'Mensuelle')], default=0, verbose_name='cat??gorie de p??riodes'),
        ),
    ]
