# Generated by Django 3.1.4 on 2021-01-16 11:40

from decimal import Decimal
from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import mod_transport.submodels.model_vehicule_activite


class Migration(migrations.Migration):

    dependencies = [
        ('mod_crm', '0006_auto_20190110_1254'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('mod_transport', '0010_vehiculesouscategorie_ai_cout_duplicata_carte_professionnelle'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vehiculeactivite',
            name='fichier_formulaire_arret',
            field=models.FileField(blank=True, max_length=255, null=True, upload_to=mod_transport.submodels.model_vehicule_activite.path_fichier_formulaire_arret_activite_vehicule),
        ),
        migrations.CreateModel(
            name='VehiculeActiviteArret',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('numero_activite', models.CharField(max_length=30, unique=True)),
                ('date_debut', models.DateField()),
                ('chassis', models.CharField(blank=True, max_length=17, null=True)),
                ('solde_depart', models.DecimalField(decimal_places=2, default=0.0, max_digits=10, validators=[django.core.validators.MinValueValidator(Decimal('0.00'))])),
                ('fichier_carterose', models.FileField(blank=True, max_length=255, null=True, upload_to=mod_transport.submodels.model_vehicule_activite.path_fichier_vehicule_activite_carterose)),
                ('fichier_autorisation', models.FileField(blank=True, max_length=255, null=True, upload_to=mod_transport.submodels.model_vehicule_activite.path_fichier_vehicule_activite_autorisation)),
                ('motif', models.CharField(blank=True, max_length=100, null=True)),
                ('date_fin', models.DateField(blank=True, null=True)),
                ('fichier_formulaire_arret', models.FileField(blank=True, max_length=255, null=True, upload_to=mod_transport.submodels.model_vehicule_activite.path_fichier_formulaire_arret_activite_vehicule)),
                ('numero_carte_physique', models.CharField(blank=True, max_length=10, null=True)),
                ('nombre_impression', models.PositiveSmallIntegerField(default=0)),
                ('date_create', models.DateTimeField(auto_now_add=True)),
                ('date_update', models.DateTimeField(null=True)),
                ('date_validate', models.DateTimeField(null=True)),
                ('date_print', models.DateTimeField(null=True)),
                ('note', models.CharField(blank=True, max_length=255, null=True)),
                ('date_note', models.DateTimeField(null=True)),
                ('reponse_note', models.CharField(blank=True, max_length=255, null=True)),
                ('demande_annulation_validation', models.BooleanField(default=False)),
                ('date_cancel', models.DateTimeField(null=True)),
                ('date_ecriture', models.DateTimeField(null=True)),
                ('contribuable', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mod_crm.contribuable')),
                ('user_arret', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='vehiculeactivitearret_requests_arret', to=settings.AUTH_USER_MODEL)),
                ('user_cancel', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='vehiculeactivitearret_requests_cancel', to=settings.AUTH_USER_MODEL)),
                ('user_create', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='vehiculeactivitearret_requests_created', to=settings.AUTH_USER_MODEL)),
                ('user_ecriture', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='vehiculeactivitearret_requests_ecriture', to=settings.AUTH_USER_MODEL)),
                ('user_note', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='vehiculeactivitearret_requests_note', to=settings.AUTH_USER_MODEL)),
                ('user_print', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='vehiculeactivitearret_requests_print', to=settings.AUTH_USER_MODEL)),
                ('user_update', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='vehiculeactivitearret_requests_updated', to=settings.AUTH_USER_MODEL)),
                ('user_validate', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='vehiculeactivitearret_requests_validate', to=settings.AUTH_USER_MODEL)),
                ('vehicule', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mod_transport.vehicule')),
            ],
        ),
    ]
