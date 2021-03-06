# Generated by Django 2.0.7 on 2018-10-23 08:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mod_activite', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='activiteexceptionnel',
            name='note',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='allocationespacepublique',
            name='note',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='allocationpanneaupublicitaire',
            name='note',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='allocationplacemarche',
            name='note',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='arretservice',
            name='note',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='baseactivite',
            name='note',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='publicitemurcloture',
            name='note',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='visitesitetouristique',
            name='note',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
