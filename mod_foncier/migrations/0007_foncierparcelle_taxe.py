# Generated by Django 2.0.7 on 2018-11-05 08:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        
        ('mod_foncier', '0006_auto_20181101_2330'),
    ]

    operations = [
        migrations.AddField(
            model_name='foncierparcelle',
            name='taxe',
            field=models.ForeignKey(default=337, on_delete=django.db.models.deletion.CASCADE, to='mod_finance.Taxe'),
            preserve_default=False,
        ),
    ]
