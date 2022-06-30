# Generated by Django 3.1.7 on 2022-06-14 09:46

from decimal import Decimal
from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import mod_finance.submodels.model_imposition


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("mod_finance", "0138_auto_20220614_1129"),
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
            model_name="avisimposition",
            name="entity",
            field=models.PositiveSmallIntegerField(
                choices=[
                    (9, "Location batiments municipaux"),
                    (13, "Django-Model:VehiculeProprietaire"),
                    (10, "Django-Model:FoncierParcelle"),
                    (17, "Django-Model:VehiculeProprietaireDuplicata"),
                    (14, "Django-Model:BaseActiviteDuplicata"),
                    (4, "Django-Model:VisiteSiteTouristique"),
                    (16, "Django-Model:VehiculeActiviteDuplicata"),
                    (5, "Django-Model:AllocationEspacePublique"),
                    (18, "Django-Model:BetailsPropriete"),
                    (15, "Django-Model:FoncierParcelleDuplicata"),
                    (7, "Django-Model:PubliciteMurCloture"),
                    (6, "Django-Model:AllocationPanneauPublicitaire"),
                    (8, "Django-Model:AllocationPlaceMarche"),
                    (1, "Django-Model:Standard"),
                    (11, "Django-Model:VehiculeActivite"),
                    (2, "Django-Model:Marche"),
                    (12, "Django-Model:VehiculeActivite"),
                    (3, "Django-Model:ActiviteExceptionnel"),
                ],
                null=True,
            ),
        ),
        migrations.AlterField(
            model_name="noteimposition",
            name="entity",
            field=models.PositiveSmallIntegerField(
                choices=[
                    (9, "Location batiments municipaux"),
                    (13, "Django-Model:VehiculeProprietaire"),
                    (10, "Django-Model:FoncierParcelle"),
                    (17, "Django-Model:VehiculeProprietaireDuplicata"),
                    (14, "Django-Model:BaseActiviteDuplicata"),
                    (4, "Django-Model:VisiteSiteTouristique"),
                    (16, "Django-Model:VehiculeActiviteDuplicata"),
                    (5, "Django-Model:AllocationEspacePublique"),
                    (18, "Django-Model:BetailsPropriete"),
                    (15, "Django-Model:FoncierParcelleDuplicata"),
                    (7, "Django-Model:PubliciteMurCloture"),
                    (6, "Django-Model:AllocationPanneauPublicitaire"),
                    (8, "Django-Model:AllocationPlaceMarche"),
                    (1, "Django-Model:Standard"),
                    (11, "Django-Model:VehiculeActivite"),
                    (2, "Django-Model:Marche"),
                    (12, "Django-Model:VehiculeActivite"),
                    (3, "Django-Model:ActiviteExceptionnel"),
                ],
                null=True,
            ),
        ),
        migrations.AlterField(
            model_name="noteimpositiondelete",
            name="entity",
            field=models.PositiveSmallIntegerField(
                choices=[
                    (9, "Location batiments municipaux"),
                    (13, "Django-Model:VehiculeProprietaire"),
                    (10, "Django-Model:FoncierParcelle"),
                    (17, "Django-Model:VehiculeProprietaireDuplicata"),
                    (14, "Django-Model:BaseActiviteDuplicata"),
                    (4, "Django-Model:VisiteSiteTouristique"),
                    (16, "Django-Model:VehiculeActiviteDuplicata"),
                    (5, "Django-Model:AllocationEspacePublique"),
                    (18, "Django-Model:BetailsPropriete"),
                    (15, "Django-Model:FoncierParcelleDuplicata"),
                    (7, "Django-Model:PubliciteMurCloture"),
                    (6, "Django-Model:AllocationPanneauPublicitaire"),
                    (8, "Django-Model:AllocationPlaceMarche"),
                    (1, "Django-Model:Standard"),
                    (11, "Django-Model:VehiculeActivite"),
                    (2, "Django-Model:Marche"),
                    (12, "Django-Model:VehiculeActivite"),
                    (3, "Django-Model:ActiviteExceptionnel"),
                ],
                null=True,
            ),
        ),
        migrations.AlterField(
            model_name="periode",
            name="element",
            field=models.IntegerField(
                choices=[
                    (12, "DECEMBRE"),
                    (13, "1er TRIMESTRE"),
                    (2, "FEVRIER"),
                    (6, "JUIN"),
                    (18, "2e SEMESTRE"),
                    (7, "JUILLET"),
                    (3, "MARS"),
                    (16, "4e TRIMESTRE"),
                    (19, "ANNEE"),
                    (5, "MAI"),
                    (8, "AOUT"),
                    (9, "SEPTEMBRE"),
                    (17, "1er SEMESTRE"),
                    (10, "OCTOBRE"),
                    (14, "2e TRIMESTRE"),
                    (4, "AVRIL"),
                    (11, "NOVEMBRE"),
                    (1, "JANVIER"),
                    (15, "3e TRIMESTRE"),
                ],
                verbose_name="Elements de période",
            ),
        ),
        migrations.AlterField(
            model_name="periodetype",
            name="categorie",
            field=models.IntegerField(
                choices=[
                    (0, "Autre"),
                    (1, "Mensuelle"),
                    (3, "Semestrielle"),
                    (4, "Annuelle"),
                    (2, "Trimestrielle"),
                ],
                default=0,
                verbose_name="catégorie de périodes",
            ),
        ),
        migrations.CreateModel(
            name="AvisImpositionPaiement",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("ref_paiement", models.CharField(max_length=20)),
                ("date_paiement", models.DateTimeField()),
                (
                    "montant",
                    models.DecimalField(
                        decimal_places=2,
                        max_digits=10,
                        validators=[
                            django.core.validators.MinValueValidator(Decimal("0"))
                        ],
                    ),
                ),
                (
                    "montant_excedant",
                    models.DecimalField(
                        decimal_places=2,
                        default=0,
                        max_digits=10,
                        validators=[
                            django.core.validators.MinValueValidator(Decimal("0"))
                        ],
                    ),
                ),
                (
                    "fichier_paiement",
                    models.FileField(
                        null=True,
                        upload_to=mod_finance.submodels.model_imposition.path_bordereau_ni_file,
                    ),
                ),
                ("note", models.CharField(blank=True, max_length=255, null=True)),
                ("date_note", models.DateTimeField(null=True)),
                (
                    "reponse_note",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                ("demande_annulation_validation", models.BooleanField(default=False)),
                ("date_cancel", models.DateTimeField(null=True)),
                ("date_create", models.DateTimeField(auto_now_add=True)),
                ("date_update", models.DateTimeField(null=True)),
                ("date_validate", models.DateTimeField(null=True)),
                (
                    "agence",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="mod_finance.agence",
                    ),
                ),
                (
                    "avis_imposition",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="mod_finance.avisimposition",
                    ),
                ),
                (
                    "user_cancel",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="avisimpositionpaiement_requests_cancel",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "user_create",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="avisimpositionpaiement_requests_created",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "user_note",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="avisimpositionpaiement_requests_note",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "user_update",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="avisimpositionpaiement_requests_updated",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "user_validate",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="avisimpositionpaiement_requests_validate",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "ordering": ("-id",),
                "unique_together": {("agence", "ref_paiement")},
                "index_together": {("agence", "ref_paiement")},
            },
        ),
    ]