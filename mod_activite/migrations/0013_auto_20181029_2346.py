# Generated by Django 2.0.7 on 2018-10-29 21:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mod_foncier', '0004_auto_20181029_0824'),
        ('mod_activite', '0012_auto_20181029_0824'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='allocationpanneaupublicitaire',
            name='adresse',
        ),
        migrations.RemoveField(
            model_name='allocationpanneaupublicitaire',
            name='adresse_precise',
        ),
        migrations.RemoveField(
            model_name='allocationpanneaupublicitaire',
            name='numero_rueavenue',
        ),
        migrations.AddField(
            model_name='allocationpanneaupublicitaire',
            name='parcelle_publique',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='mod_foncier.FoncierParcellePublique'),
            preserve_default=False,
        ),
    ]
