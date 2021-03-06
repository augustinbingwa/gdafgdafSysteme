# Generated by Django 2.0.7 on 2019-01-07 21:40

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import mod_helpers.submodels.model_user_profile


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('mod_helpers', '0004_auto_20190105_1628'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tel', models.CharField(blank=True, max_length=20, null=True)),
                ('email', models.CharField(blank=True, max_length=70, null=True)),
                ('fonction', models.CharField(blank=True, max_length=255, null=True)),
                ('avatar', models.ImageField(blank=True, max_length=255, null=True, upload_to=mod_helpers.submodels.model_user_profile.path_photo_user)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
