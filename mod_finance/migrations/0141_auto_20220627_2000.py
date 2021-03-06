# Generated by Django 3.1.7 on 2022-06-27 18:00

from decimal import Decimal
from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import mod_finance.submodels.model_imposition


class Migration(migrations.Migration):

    dependencies = [
        ('mod_crm', '0006_auto_20190110_1254'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('mod_finance', '0140_auto_20220614_1152'),
    ]

    operations = [
        migrations.CreateModel(
            name='UpdateFileUpload',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('update_file_info', models.FileField(null=True, upload_to=mod_finance.submodels.model_imposition.path_update_ni_info_file)),
                ('nbr_update', models.IntegerField(null=True)),
                ('ni_id', models.IntegerField(null=True)),
                ('status', models.IntegerField(default=0)),
                ('commentaire', models.TextField(null=True)),
            ],
            options={
                'ordering': ('-id',),
            },
        ),
        migrations.AlterField(
            model_name='avisimposition',
            name='entity',
            field=models.PositiveSmallIntegerField(choices=[(9, 'Django-Model:Location batiments municipaux'), (13, 'Django-Model:VehiculeProprietaire'), (15, 'Django-Model:FoncierParcelleDuplicata'), (11, 'Django-Model:VehiculeActivite'), (19, 'Django-Model:Attestation'), (1, 'Django-Model:Standard'), (4, 'Django-Model:VisiteSiteTouristique'), (17, 'Django-Model:VehiculeProprietaireDuplicata'), (3, 'Django-Model:ActiviteExceptionnel'), (8, 'Django-Model:AllocationPlaceMarche'), (20, 'Django-Model:Acte'), (16, 'Django-Model:VehiculeActiviteDuplicata'), (2, 'Django-Model:Marche'), (10, 'Django-Model:FoncierParcelle'), (6, 'Django-Model:AllocationPanneauPublicitaire'), (5, 'Django-Model:AllocationEspacePublique'), (12, 'Django-Model:VehiculeActivite'), (7, 'Django-Model:PubliciteMurCloture'), (14, 'Django-Model:BaseActiviteDuplicata'), (18, 'Django-Model:BetailsPropriete')], null=True),
        ),
        migrations.AlterField(
            model_name='noteimposition',
            name='entity',
            field=models.PositiveSmallIntegerField(choices=[(9, 'Django-Model:Location batiments municipaux'), (13, 'Django-Model:VehiculeProprietaire'), (15, 'Django-Model:FoncierParcelleDuplicata'), (11, 'Django-Model:VehiculeActivite'), (19, 'Django-Model:Attestation'), (1, 'Django-Model:Standard'), (4, 'Django-Model:VisiteSiteTouristique'), (17, 'Django-Model:VehiculeProprietaireDuplicata'), (3, 'Django-Model:ActiviteExceptionnel'), (8, 'Django-Model:AllocationPlaceMarche'), (20, 'Django-Model:Acte'), (16, 'Django-Model:VehiculeActiviteDuplicata'), (2, 'Django-Model:Marche'), (10, 'Django-Model:FoncierParcelle'), (6, 'Django-Model:AllocationPanneauPublicitaire'), (5, 'Django-Model:AllocationEspacePublique'), (12, 'Django-Model:VehiculeActivite'), (7, 'Django-Model:PubliciteMurCloture'), (14, 'Django-Model:BaseActiviteDuplicata'), (18, 'Django-Model:BetailsPropriete')], null=True),
        ),
        migrations.AlterField(
            model_name='noteimpositiondelete',
            name='entity',
            field=models.PositiveSmallIntegerField(choices=[(9, 'Django-Model:Location batiments municipaux'), (13, 'Django-Model:VehiculeProprietaire'), (15, 'Django-Model:FoncierParcelleDuplicata'), (11, 'Django-Model:VehiculeActivite'), (19, 'Django-Model:Attestation'), (1, 'Django-Model:Standard'), (4, 'Django-Model:VisiteSiteTouristique'), (17, 'Django-Model:VehiculeProprietaireDuplicata'), (3, 'Django-Model:ActiviteExceptionnel'), (8, 'Django-Model:AllocationPlaceMarche'), (20, 'Django-Model:Acte'), (16, 'Django-Model:VehiculeActiviteDuplicata'), (2, 'Django-Model:Marche'), (10, 'Django-Model:FoncierParcelle'), (6, 'Django-Model:AllocationPanneauPublicitaire'), (5, 'Django-Model:AllocationEspacePublique'), (12, 'Django-Model:VehiculeActivite'), (7, 'Django-Model:PubliciteMurCloture'), (14, 'Django-Model:BaseActiviteDuplicata'), (18, 'Django-Model:BetailsPropriete')], null=True),
        ),
        migrations.AlterField(
            model_name='periode',
            name='element',
            field=models.IntegerField(choices=[(15, '3e TRIMESTRE'), (14, '2e TRIMESTRE'), (10, 'OCTOBRE'), (16, '4e TRIMESTRE'), (3, 'MARS'), (12, 'DECEMBRE'), (6, 'JUIN'), (11, 'NOVEMBRE'), (7, 'JUILLET'), (18, '2e SEMESTRE'), (4, 'AVRIL'), (5, 'MAI'), (19, 'ANNEE'), (17, '1er SEMESTRE'), (8, 'AOUT'), (2, 'FEVRIER'), (13, '1er TRIMESTRE'), (1, 'JANVIER'), (9, 'SEPTEMBRE')], verbose_name='Elements de p??riode'),
        ),
        migrations.AlterField(
            model_name='periodetype',
            name='categorie',
            field=models.IntegerField(choices=[(0, 'Autre'), (4, 'Annuelle'), (2, 'Trimestrielle'), (1, 'Mensuelle'), (3, 'Semestrielle')], default=0, verbose_name='cat??gorie de p??riodes'),
        ),
        migrations.CreateModel(
            name='CompteContribuable',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=250)),
                ('ref_paiement', models.CharField(max_length=50)),
                ('date_paiement', models.DateTimeField()),
                ('Solde', models.DecimalField(decimal_places=2, max_digits=10, validators=[django.core.validators.MinValueValidator(Decimal('0'))])),
                ('date_create', models.DateTimeField(auto_now_add=True)),
                ('date_update', models.DateTimeField(null=True)),
                ('agence', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mod_finance.agence')),
                ('contribuable', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mod_crm.contribuable')),
                ('user_create', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comptecontribuable_requests_created', to=settings.AUTH_USER_MODEL)),
                ('user_update', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='comptecontribuable_requests_updated', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('-id',),
            },
        ),
    ]
