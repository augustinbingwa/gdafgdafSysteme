# Generated by Django 2.0.7 on 2019-01-04 08:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mod_helpers', '0002_auto_20190104_0408'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notearchive',
            name='entity',
            field=models.CharField(max_length=255),
        ),
    ]