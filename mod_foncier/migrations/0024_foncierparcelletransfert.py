# Generated by Django 2.0.7 on 2020-05-05 14:52

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import mod_foncier.submodels.model_foncier_parcelle


class Migration(migrations.Migration):

    dependencies = [
        ('mod_finance', '0121_auto_20200505_1652'),
        ('mod_crm', '0006_auto_20190110_1254'),
        ('mod_parametrage', '0107_auto_20200505_1652'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('mod_foncier', '0023_foncierexpertise_etat'),
    ]

    operations = [
        migrations.CreateModel(
            name='FoncierParcelleTransfert',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('numero_parcelle', models.CharField(max_length=15, unique=True)),
                ('contribuable_nv', models.IntegerField(default=0)),
                ('numero_police', models.CharField(blank=True, max_length=15, null=True)),
                ('fichier_declaration', models.FileField(blank=True, max_length=255, null=True, upload_to=mod_foncier.submodels.model_foncier_parcelle.path_fichier_declaration)),
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
                ('accessibilite', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mod_parametrage.Accessibilite')),
                ('adresse', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mod_parametrage.Quartier')),
                ('contribuable_exi', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mod_crm.Contribuable')),
                ('numero_rueavenue', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mod_parametrage.RueOuAvenue')),
                ('taxe', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mod_finance.Taxe')),
                ('user_cancel', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='foncierparcelletransfert_requests_cancel', to=settings.AUTH_USER_MODEL)),
                ('user_create', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='foncierparcelletransfert_requests_created', to=settings.AUTH_USER_MODEL)),
                ('user_note', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='foncierparcelletransfert_requests_note', to=settings.AUTH_USER_MODEL)),
                ('user_print', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='foncierparcelletransfert_requests_print', to=settings.AUTH_USER_MODEL)),
                ('user_update', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='foncierparcelletransfert_requests_updated', to=settings.AUTH_USER_MODEL)),
                ('user_validate', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='foncierparcelletransfert_requests_validate', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('-id',),
            },
        ),
    ]
