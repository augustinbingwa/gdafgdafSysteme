# Generated by Django 2.0.7 on 2018-10-11 09:31

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Chrono',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('prefixe', models.CharField(max_length=3, unique=True)),
                ('fonctionalite', models.CharField(max_length=50, unique=True)),
                ('annee', models.BooleanField(default=True)),
                ('mois', models.BooleanField(default=True)),
                ('nombre', models.PositiveSmallIntegerField()),
                ('last_chrono', models.CharField(blank=True, max_length=50)),
            ],
            options={
                'ordering': ('fonctionalite', 'annee', 'mois'),
            },
        ),
    ]
