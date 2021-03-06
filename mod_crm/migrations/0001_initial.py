# Generated by Django 2.0.7 on 2018-10-11 09:31

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import mod_crm.submodels.model_contribuable


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('mod_parametrage', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Contribuable',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('matricule', models.CharField(max_length=17, unique=True)),
                ('nom', models.CharField(max_length=100)),
                ('adresse_exacte', models.CharField(blank=True, max_length=255, null=True)),
                ('numero_police', models.CharField(blank=True, max_length=15, null=True)),
                ('code_postal', models.CharField(blank=True, max_length=5, null=True)),
                ('tel', models.CharField(blank=True, max_length=20, null=True)),
                ('email', models.CharField(blank=True, max_length=70, null=True)),
                ('nif_numero', models.CharField(blank=True, max_length=15, null=True)),
                ('nif_file', models.FileField(blank=True, max_length=255, null=True, upload_to=mod_crm.submodels.model_contribuable.path_nif_file)),
                ('date_create', models.DateTimeField(auto_now_add=True)),
                ('date_update', models.DateTimeField(null=True)),
                ('date_validate', models.DateTimeField(null=True)),
            ],
            options={
                'ordering': ('-id',),
            },
        ),
        migrations.CreateModel(
            name='PersonneMorale',
            fields=[
                ('contribuable_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='mod_crm.Contribuable')),
                ('type_caractere', models.IntegerField(choices=[(0, 'Commercial'), (1, 'Sans but lucratif')], default=0)),
                ('rc_numero', models.CharField(blank=True, max_length=50)),
                ('rc_file', models.FileField(blank=True, max_length=255, null=True, upload_to=mod_crm.submodels.model_contribuable.path_rc_file)),
            ],
            bases=('mod_crm.contribuable',),
        ),
        migrations.CreateModel(
            name='PersonnePhysique',
            fields=[
                ('contribuable_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='mod_crm.Contribuable')),
                ('sexe', models.IntegerField(choices=[(0, 'F??minin'), (1, 'Masculin')])),
                ('date_naiss', models.DateField()),
                ('lieu_naiss', models.CharField(max_length=250)),
                ('identite', models.IntegerField(choices=[(0, 'CNI'), (1, 'Passeport')])),
                ('identite_numero', models.CharField(max_length=50, unique=True)),
                ('identite_file', models.FileField(blank=True, max_length=255, null=True, upload_to=mod_crm.submodels.model_contribuable.path_identite_file)),
                ('photo_file', models.FileField(blank=True, max_length=255, null=True, upload_to=mod_crm.submodels.model_contribuable.path_photo)),
            ],
            bases=('mod_crm.contribuable',),
        ),
        migrations.AddField(
            model_name='contribuable',
            name='adresse',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='mod_parametrage.Quartier'),
        ),
        migrations.AddField(
            model_name='contribuable',
            name='numero_rueavenue',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='mod_parametrage.RueOuAvenue'),
        ),
        migrations.AddField(
            model_name='contribuable',
            name='user_create',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='contribuable_requests_created', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='contribuable',
            name='user_update',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='contribuable_requests_updated', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='contribuable',
            name='user_validate',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='contribuable_requests_validate', to=settings.AUTH_USER_MODEL),
        ),
    ]
