# Generated by Django 2.0.7 on 2018-10-23 08:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mod_crm', '0002_auto_20181019_1641'),
    ]

    operations = [
        migrations.AddField(
            model_name='contribuable',
            name='note',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
