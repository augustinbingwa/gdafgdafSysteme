# Generated by Django 2.0.7 on 2018-10-11 09:31

from decimal import Decimal
from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import mod_finance.submodels.model_imposition


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('mod_crm', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Agence',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=10, unique=True)),
                ('sigle', models.CharField(max_length=10, unique=True)),
                ('nom', models.CharField(max_length=100, unique=True)),
                ('compte', models.CharField(max_length=15, unique=True)),
            ],
            options={
                'ordering': ('code',),
            },
        ),
        migrations.CreateModel(
            name='AvisImposition',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reference', models.CharField(max_length=25, unique=True)),
                ('nom', models.CharField(blank=True, default='', max_length=100, null=True)),
                ('taxe_montant', models.DecimalField(decimal_places=2, max_digits=10, validators=[django.core.validators.MinValueValidator(Decimal('0.00'))])),
                ('nombre_copie', models.PositiveSmallIntegerField(default=1)),
                ('montant_total', models.DecimalField(decimal_places=2, max_digits=10, validators=[django.core.validators.MinValueValidator(Decimal('0.00'))])),
                ('validite', models.PositiveSmallIntegerField(default=1)),
                ('entity', models.IntegerField(choices=[(5, 'Django-Model:AllocationEspacePublique'), (10, 'Django-Model:FoncierParcelle'), (1, 'Django-Model:Standard'), (7, 'Django-Model:PubliciteMurCloture'), (12, 'Django-Model:VehiculeActivite'), (18, 'Django-Model:BetailsPropriete'), (17, 'Django-Model:VehiculeProprietaireDuplicata'), (14, 'Django-Model:BaseActiviteDuplicata'), (6, 'Django-Model:AllocationPanneauPublicitaire'), (8, 'Django-Model:AllocationPlaceMarche'), (3, 'Django-Model:ActiviteExceptionnel'), (13, 'Django-Model:VehiculeProprietaire'), (15, 'Django-Model:FoncierParcelleDuplicata'), (16, 'Django-Model:VehiculeActiviteDuplicata'), (9, 'Location batiments municipaux'), (4, 'Django-Model:VisiteSiteTouristique'), (2, 'Django-Model:Marche'), (11, 'Django-Model:VehiculeActivite')], null=True)),
                ('entity_id', models.PositiveSmallIntegerField(null=True)),
                ('libelle', models.TextField(max_length=512)),
                ('ref_paiement', models.CharField(max_length=15, null=True)),
                ('date_paiement', models.DateTimeField(null=True)),
                ('fichier_paiement', models.FileField(null=True, upload_to=mod_finance.submodels.model_imposition.path_bordereau_ai_file)),
                ('date_create', models.DateTimeField(auto_now_add=True)),
                ('date_update', models.DateTimeField(null=True)),
                ('date_validate', models.DateTimeField(null=True)),
                ('date_print', models.DateTimeField(null=True)),
                ('agence', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='mod_finance.Agence')),
                ('contribuable', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='mod_crm.Contribuable')),
            ],
            options={
                'ordering': ('-id',),
            },
        ),
        migrations.CreateModel(
            name='NoteImposition',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reference', models.CharField(max_length=25, unique=True)),
                ('entity', models.IntegerField(choices=[(5, 'Django-Model:AllocationEspacePublique'), (10, 'Django-Model:FoncierParcelle'), (1, 'Django-Model:Standard'), (7, 'Django-Model:PubliciteMurCloture'), (12, 'Django-Model:VehiculeActivite'), (18, 'Django-Model:BetailsPropriete'), (17, 'Django-Model:VehiculeProprietaireDuplicata'), (14, 'Django-Model:BaseActiviteDuplicata'), (6, 'Django-Model:AllocationPanneauPublicitaire'), (8, 'Django-Model:AllocationPlaceMarche'), (3, 'Django-Model:ActiviteExceptionnel'), (13, 'Django-Model:VehiculeProprietaire'), (15, 'Django-Model:FoncierParcelleDuplicata'), (16, 'Django-Model:VehiculeActiviteDuplicata'), (9, 'Location batiments municipaux'), (4, 'Django-Model:VisiteSiteTouristique'), (2, 'Django-Model:Marche'), (11, 'Django-Model:VehiculeActivite')], null=True)),
                ('entity_id', models.PositiveSmallIntegerField(null=True)),
                ('annee', models.PositiveSmallIntegerField(default=2018, validators=[django.core.validators.MinValueValidator(2014), django.core.validators.MaxValueValidator(9999)])),
                ('libelle', models.TextField(max_length=1024)),
                ('taxe_montant', models.DecimalField(decimal_places=2, max_digits=10, validators=[django.core.validators.MinValueValidator(Decimal('0.00'))])),
                ('taxe_montant_paye', models.DecimalField(decimal_places=2, default=0.0, max_digits=10, validators=[django.core.validators.MinValueValidator(Decimal('0.00'))])),
                ('numero_carte_physique', models.CharField(blank=True, max_length=10, null=True)),
                ('nombre_impression', models.PositiveSmallIntegerField(default=0)),
                ('date_create', models.DateTimeField(auto_now_add=True)),
                ('date_update', models.DateTimeField(null=True)),
                ('date_validate', models.DateTimeField(null=True)),
                ('date_print', models.DateTimeField(null=True)),
                ('contribuable', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='mod_crm.Contribuable')),
            ],
            options={
                'ordering': ('-id',),
            },
        ),
        migrations.CreateModel(
            name='NoteImpositionPaiement',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ref_paiement', models.CharField(max_length=15)),
                ('date_paiement', models.DateTimeField()),
                ('montant_tranche', models.DecimalField(decimal_places=2, max_digits=10, validators=[django.core.validators.MinValueValidator(Decimal('0.00'))])),
                ('fichier_paiement', models.FileField(null=True, upload_to=mod_finance.submodels.model_imposition.path_bordereau_ni_file)),
                ('date_create', models.DateTimeField(auto_now_add=True)),
                ('date_update', models.DateTimeField(null=True)),
                ('date_validate', models.DateTimeField(null=True)),
                ('agence', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mod_finance.Agence')),
                ('note_imposition', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mod_finance.NoteImposition')),
                ('user_create', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='noteimpositionpaiement_requests_created', to=settings.AUTH_USER_MODEL)),
                ('user_update', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='noteimpositionpaiement_requests_updated', to=settings.AUTH_USER_MODEL)),
                ('user_validate', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='noteimpositionpaiement_requests_validate', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('-id',),
            },
        ),
        migrations.CreateModel(
            name='Operateur',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('libelle', models.CharField(max_length=25, unique=True)),
            ],
            options={
                'ordering': ('libelle',),
            },
        ),
        migrations.CreateModel(
            name='Periode',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('element', models.IntegerField(choices=[(11, 'Novembre'), (17, '1er Semestre'), (19, 'Année'), (7, 'Juillet'), (18, '2e Semestre'), (10, 'Octobre'), (6, 'Juin'), (16, '4e Timestre'), (5, 'Mai'), (2, 'Février'), (1, 'Janvier'), (12, 'Décembre'), (9, 'Septembre'), (15, '3e Trimestre'), (8, 'Août'), (3, 'Mars'), (4, 'Avril'), (13, '1er Trimestre'), (14, '2e Trimestre')], verbose_name='Elements de période')),
            ],
            options={
                'ordering': ('periode_type', 'element'),
            },
        ),
        migrations.CreateModel(
            name='PeriodeType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('libelle', models.CharField(max_length=25, unique=True)),
                ('temps', models.BooleanField()),
                ('categorie', models.IntegerField(choices=[(4, 'Annuelle'), (2, 'Trimestrielle'), (1, 'Mensuelle'), (3, 'Semestrielle'), (0, 'Autre')], default=0, verbose_name='catégorie de périodes')),
            ],
            options={
                'ordering': ('id',),
            },
        ),
        migrations.CreateModel(
            name='Taxe',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=5, unique=True)),
                ('libelle', models.CharField(max_length=100, unique=True, verbose_name='Matière imposable')),
                ('nom_activite', models.CharField(blank=True, max_length=100, null=True)),
                ('type_tarif', models.IntegerField(choices=[(0, 'Forfaitaire'), (1, 'Pourcentage'), (2, 'Variable')], verbose_name='Type du tarif')),
                ('tarif', models.DecimalField(decimal_places=0, max_digits=10, validators=[django.core.validators.MinValueValidator(Decimal('0.00'))])),
                ('imputation_budgetaire', models.CharField(max_length=10, verbose_name='Imputation budgétaire')),
                ('commentaire', models.TextField(blank=True, max_length=1024, null=True)),
                ('taxe_filter', models.IntegerField(choices=[(0, "Autres Avis d'imposition"), (1, "Avis d'impositon Administratif"), (2, "Avis d'impositon des documents financiers"), (3, 'Activite Standard-Marché'), (4, 'Activité exceptionnelle'), (5, 'Visite site touristique'), (6, 'Allocation Espace publique'), (7, 'Allocation panneau publicitaire'), (8, 'Publicité sur les murs et clôtures'), (11, 'Impôts fonciers'), (9, 'Allocation de place dans le marché'), (10, 'Location batiments municipaux'), (12, 'Activité sur les transports rémunérés'), (13, 'Droit de stationnement'), (14, 'Taxes sur les véhicule de propriété'), (15, 'Taxes sur les gros bétails')], default=0, verbose_name='Type de taxe')),
            ],
            options={
                'ordering': ('code',),
            },
        ),
        migrations.CreateModel(
            name='TaxeCategorie',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('libelle', models.CharField(max_length=100, unique=True, verbose_name='Libellé de la catégorie de taxes ')),
                ('type_impot', models.IntegerField(choices=[(0, "Avis d'imposition"), (1, "Note d'imposition")], verbose_name="Type d'impôt")),
            ],
            options={
                'ordering': ('id',),
            },
        ),
        migrations.AddField(
            model_name='taxe',
            name='categorie_taxe',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mod_finance.TaxeCategorie', verbose_name='Catégorie des taxes'),
        ),
        migrations.AddField(
            model_name='taxe',
            name='periode_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mod_finance.PeriodeType'),
        ),
        migrations.AddField(
            model_name='periode',
            name='periode_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mod_finance.PeriodeType'),
        ),
        migrations.AddField(
            model_name='noteimposition',
            name='periode',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mod_finance.Periode'),
        ),
        migrations.AddField(
            model_name='noteimposition',
            name='taxe',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mod_finance.Taxe'),
        ),
        migrations.AddField(
            model_name='noteimposition',
            name='user_create',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='noteimposition_requests_created', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='noteimposition',
            name='user_print',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='noteimposition_requests_print', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='noteimposition',
            name='user_update',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='noteimposition_requests_updated', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='noteimposition',
            name='user_validate',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='noteimposition_requests_validate', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='avisimposition',
            name='taxe',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mod_finance.Taxe'),
        ),
        migrations.AddField(
            model_name='avisimposition',
            name='user_create',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='avisimposition_requests_created', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='avisimposition',
            name='user_print',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='avisimposition_requests_print', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='avisimposition',
            name='user_update',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='avisimposition_requests_updated', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='avisimposition',
            name='user_validate',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='avisimposition_requests_validate', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='agence',
            name='operateur',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mod_finance.Operateur'),
        ),
        migrations.AlterUniqueTogether(
            name='noteimpositionpaiement',
            unique_together={('agence', 'ref_paiement')},
        ),
        migrations.AlterIndexTogether(
            name='noteimpositionpaiement',
            index_together={('agence', 'ref_paiement')},
        ),
        migrations.AlterUniqueTogether(
            name='avisimposition',
            unique_together={('agence', 'ref_paiement')},
        ),
        migrations.AlterIndexTogether(
            name='avisimposition',
            index_together={('agence', 'ref_paiement')},
        ),
    ]
