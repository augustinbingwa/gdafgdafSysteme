# Generated by Django 2.0.7 on 2018-10-26 12:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mod_activite', '0009_auto_20181024_1134'),
    ]

    operations = [
        migrations.AlterField(
            model_name='publicitemurcloture',
            name='type_publicite',
            field=models.IntegerField(choices=[(0, 'Mûr'), (1, 'Clôture')]),
        ),
    ]
