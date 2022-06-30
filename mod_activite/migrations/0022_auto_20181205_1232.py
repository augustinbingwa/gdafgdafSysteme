# Generated by Django 2.0.7 on 2018-12-05 10:32

from decimal import Decimal
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mod_activite', '0021_auto_20181119_1118'),
    ]

    operations = [
        migrations.AddField(
            model_name='allocationplacemarche',
            name='caution_montant',
            field=models.DecimalField(decimal_places=0, default=0, max_digits=10, validators=[django.core.validators.MinValueValidator(Decimal('0'))]),
        ),
        migrations.AddField(
            model_name='allocationplacemarche',
            name='caution_nombre_mois',
            field=models.PositiveSmallIntegerField(default=0),
        ),
    ]
