# Generated by Django 2.0.7 on 2018-11-05 11:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mod_foncier', '0007_foncierparcelle_taxe'),
    ]

    operations = [
        migrations.AlterField(
            model_name='foncierexpertise',
            name='superficie_non_batie',
            field=models.PositiveSmallIntegerField(default=0),
        ),
    ]