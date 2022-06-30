# Generated by Django 2.0.7 on 2018-10-23 21:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mod_finance', '0008_auto_20181023_2308'),
        ('mod_activite', '0003_auto_20181023_2256'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='activiteexceptionnelle',
            name='ai_reference',
        ),
        migrations.AddField(
            model_name='activiteexceptionnelle',
            name='taxe',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='mod_finance.Taxe'),
            preserve_default=False,
        ),
    ]
