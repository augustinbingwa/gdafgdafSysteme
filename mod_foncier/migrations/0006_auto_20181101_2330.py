# Generated by Django 2.0.7 on 2018-11-01 21:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mod_foncier', '0005_foncierparcellepublique_usage'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='foncieraccessibilite',
            options={'ordering': ('id',)},
        ),
        migrations.AlterModelOptions(
            name='fonciercategorie',
            options={'ordering': ('id',)},
        ),
        migrations.AlterModelOptions(
            name='foncierimpot',
            options={'ordering': ('id',)},
        ),
        migrations.AlterModelOptions(
            name='fonciertnbcategorie',
            options={'ordering': ('id',)},
        ),
        migrations.AlterModelOptions(
            name='fonciertnbimpot',
            options={'ordering': ('id',)},
        ),
        migrations.AlterModelOptions(
            name='fonciertypeconfort',
            options={'ordering': ('id',)},
        ),
        migrations.AddField(
            model_name='foncierparcelle',
            name='accessibilite',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='mod_foncier.FoncierAccessibilite'),
            preserve_default=False,
        ),
    ]