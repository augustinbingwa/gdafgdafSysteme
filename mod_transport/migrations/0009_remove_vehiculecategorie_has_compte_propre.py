# Generated by Django 2.0.7 on 2019-02-24 12:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mod_transport', '0008_vehiculesouscategorie_has_compte_propre'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='vehiculecategorie',
            name='has_compte_propre',
        ),
    ]