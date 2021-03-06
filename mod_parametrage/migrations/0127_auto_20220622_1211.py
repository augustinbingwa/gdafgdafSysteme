# Generated by Django 3.1.7 on 2022-06-22 10:11

from django.db import migrations, models
import mod_parametrage.submodels.reportfile


class Migration(migrations.Migration):

    dependencies = [
        ('mod_parametrage', '0126_auto_20220614_1152'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='reportfileupload',
            options={'ordering': ('-id',)},
        ),
        migrations.AlterField(
            model_name='notification',
            name='entity',
            field=models.PositiveSmallIntegerField(choices=[(6, 'Django-Model:AllocationPanneauPublicitaire'), (16, 'Django-Model:VehiculeActiviteDuplicata'), (18, 'Django-Model:BetailsPropriete'), (8, 'Django-Model:AllocationPlaceMarche'), (12, 'Django-Model:VehiculeActivite'), (19, 'Django-Model:Attestation'), (4, 'Django-Model:VisiteSiteTouristique'), (20, 'Django-Model:Acte'), (14, 'Django-Model:BaseActiviteDuplicata'), (2, 'Django-Model:Marche'), (17, 'Django-Model:VehiculeProprietaireDuplicata'), (9, 'Django-Model:Location batiments municipaux'), (7, 'Django-Model:PubliciteMurCloture'), (3, 'Django-Model:ActiviteExceptionnel'), (11, 'Django-Model:VehiculeActivite'), (10, 'Django-Model:FoncierParcelle'), (5, 'Django-Model:AllocationEspacePublique'), (13, 'Django-Model:VehiculeProprietaire'), (1, 'Django-Model:Standard'), (15, 'Django-Model:FoncierParcelleDuplicata')], null=True),
        ),
        migrations.AlterField(
            model_name='reportfileupload',
            name='file',
            field=models.FileField(upload_to=mod_parametrage.submodels.reportfile.path_fichier_rappot_banque),
        ),
    ]
