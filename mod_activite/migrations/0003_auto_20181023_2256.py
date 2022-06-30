# Generated by Django 2.0.7 on 2018-10-23 20:56

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import mod_activite.submodels.model_activite


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('mod_finance', '0007_auto_20181023_2256'),
        ('mod_activite', '0002_auto_20181023_1001'),
    ]

    operations = [
        migrations.CreateModel(
            name='ActiviteExceptionnelle',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('numero_activite', models.CharField(max_length=30)),
                ('nom_beneficiaire', models.CharField(max_length=50)),
                ('motif_activite', models.CharField(max_length=255)),
                ('date_delivrance', models.DateTimeField()),
                ('date_expiration', models.DateTimeField()),
                ('note', models.CharField(blank=True, max_length=255, null=True)),
                ('date_create', models.DateTimeField(auto_now_add=True)),
                ('date_update', models.DateTimeField(null=True)),
                ('date_validate', models.DateTimeField(null=True)),
                ('date_print', models.DateTimeField(null=True)),
                ('ai_reference', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mod_finance.AvisImposition')),
                ('user_create', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='activiteexceptionnelle_requests_created', to=settings.AUTH_USER_MODEL)),
                ('user_print', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='activiteexceptionnelle_requests_print', to=settings.AUTH_USER_MODEL)),
                ('user_update', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='activiteexceptionnelle_requests_updated', to=settings.AUTH_USER_MODEL)),
                ('user_validate', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='activiteexceptionnelle_requests_validate', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('-id',),
            },
        ),
        migrations.RemoveField(
            model_name='activiteexceptionnel',
            name='ai_reference',
        ),
        migrations.RemoveField(
            model_name='activiteexceptionnel',
            name='user_create',
        ),
        migrations.RemoveField(
            model_name='activiteexceptionnel',
            name='user_print',
        ),
        migrations.RemoveField(
            model_name='activiteexceptionnel',
            name='user_update',
        ),
        migrations.RemoveField(
            model_name='activiteexceptionnel',
            name='user_validate',
        ),
        migrations.AddField(
            model_name='standard',
            name='fichier_autorisation',
            field=models.FileField(blank=True, max_length=255, null=True, upload_to=mod_activite.submodels.model_activite.path_fichier_activite_standard_autorisation),
        ),
        migrations.DeleteModel(
            name='ActiviteExceptionnel',
        ),
    ]