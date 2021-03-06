# Generated by Django 2.0.7 on 2019-02-20 15:10

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('mod_foncier', '0021_auto_20190201_1633'),
    ]

    operations = [
        migrations.AddField(
            model_name='foncierexpertise',
            name='date_delete',
            field=models.DateTimeField(null=True),
        ),
        migrations.AddField(
            model_name='foncierexpertise',
            name='motif_delete',
            field=models.TextField(blank=True, max_length=1024, null=True),
        ),
        migrations.AddField(
            model_name='foncierexpertise',
            name='user_delete',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='foncierexpertise_requests_delete', to=settings.AUTH_USER_MODEL),
        ),
    ]
