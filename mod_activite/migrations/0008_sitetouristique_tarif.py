# Generated by Django 2.0.7 on 2018-10-24 08:52

from decimal import Decimal
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mod_activite', '0007_auto_20181024_0111'),
    ]

    operations = [
        migrations.AddField(
            model_name='sitetouristique',
            name='tarif',
            field=models.DecimalField(decimal_places=0, default=0, max_digits=10, validators=[django.core.validators.MinValueValidator(Decimal('0'))]),
        ),
    ]
