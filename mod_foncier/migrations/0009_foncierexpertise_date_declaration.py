# Generated by Django 2.0.7 on 2018-11-05 15:53

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mod_foncier', '0008_auto_20181105_1317'),
    ]

    operations = [
        migrations.AddField(
            model_name='foncierexpertise',
            name='date_declaration',
            field=models.DateField(default=datetime.datetime(2018, 11, 5, 17, 53, 29, 886832)),
            preserve_default=False,
        ),
    ]
