# Generated by Django 3.1.7 on 2022-02-10 15:11

from decimal import Decimal
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("mod_foncier", "0024_foncierparcelletransfert"),
    ]

    operations = [
        migrations.AddField(
            model_name="foncierexpertise",
            name="intere_montant",
            field=models.DecimalField(
                decimal_places=0,
                default=0,
                max_digits=10,
                validators=[django.core.validators.MinValueValidator(Decimal("0"))],
            ),
        ),
        migrations.AddField(
            model_name="foncierexpertise",
            name="intere_taux",
            field=models.DecimalField(
                decimal_places=1,
                default=0.0,
                max_digits=10,
                validators=[django.core.validators.MinValueValidator(Decimal("0.0"))],
            ),
        ),
        migrations.AddField(
            model_name="foncierexpertise",
            name="penalite_montant",
            field=models.DecimalField(
                decimal_places=0,
                default=0,
                max_digits=10,
                validators=[django.core.validators.MinValueValidator(Decimal("0"))],
            ),
        ),
        migrations.AddField(
            model_name="foncierexpertise",
            name="penalite_taux",
            field=models.DecimalField(
                decimal_places=1,
                default=0.0,
                max_digits=10,
                validators=[django.core.validators.MinValueValidator(Decimal("0.0"))],
            ),
        ),
    ]
