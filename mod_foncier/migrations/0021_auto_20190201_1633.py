# Generated by Django 2.0.7 on 2019-02-01 14:33

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mod_foncier', '0020_auto_20190201_1227'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fonciercaracteristique',
            name='superficie_batie',
            field=models.PositiveIntegerField(default=0, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(999999)]),
        ),
    ]
