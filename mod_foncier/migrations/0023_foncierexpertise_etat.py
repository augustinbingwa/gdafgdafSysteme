# Generated by Django 2.0.7 on 2020-02-18 18:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mod_foncier', '0022_auto_20190220_1710'),
    ]

    operations = [
        migrations.AddField(
            model_name='foncierexpertise',
            name='etat',
            field=models.BooleanField(default=True),
        ),
    ]
