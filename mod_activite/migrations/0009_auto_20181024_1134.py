# Generated by Django 2.0.7 on 2018-10-24 09:34

from decimal import Decimal
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mod_activite', '0008_sitetouristique_tarif'),
    ]

    operations = [
        migrations.RenameField(
            model_name='activiteexceptionnelle',
            old_name='piece',
            new_name='piece_nombre',
        ),
        migrations.AddField(
            model_name='activiteexceptionnelle',
            name='piece_tarif',
            field=models.DecimalField(decimal_places=0, default=0, max_digits=10, validators=[django.core.validators.MinValueValidator(Decimal('0'))]),
        ),
    ]