# Generated by Django 3.1.7 on 2022-02-09 07:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mod_parametrage', '0118_auto_20220209_0909'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notification',
            name='entity',
            field=models.PositiveSmallIntegerField(choices=[(7, 'Django-Model:PubliciteMurCloture'), (9, 'Location batiments municipaux'), (5, 'Django-Model:AllocationEspacePublique'), (13, 'Django-Model:VehiculeProprietaire'), (14, 'Django-Model:BaseActiviteDuplicata'), (12, 'Django-Model:VehiculeActivite'), (17, 'Django-Model:VehiculeProprietaireDuplicata'), (4, 'Django-Model:VisiteSiteTouristique'), (3, 'Django-Model:ActiviteExceptionnel'), (2, 'Django-Model:Marche'), (8, 'Django-Model:AllocationPlaceMarche'), (6, 'Django-Model:AllocationPanneauPublicitaire'), (18, 'Django-Model:BetailsPropriete'), (15, 'Django-Model:FoncierParcelleDuplicata'), (11, 'Django-Model:VehiculeActivite'), (1, 'Django-Model:Standard'), (10, 'Django-Model:FoncierParcelle'), (16, 'Django-Model:VehiculeActiviteDuplicata')], null=True),
        ),
        migrations.CreateModel(
            name='Fonction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('libele', models.CharField(blank=True, choices=[('MR', 'Mairie'), ('DP', 'Département'), ('SR', 'Service'), ('CM', 'Commune'), ('ZN', 'Zone'), ('QT', 'Quartier')], max_length=250, null=True, verbose_name='Localité')),
                ('title', models.CharField(blank=True, choices=[('Maire de la ville', 'Maire de la ville'), ('Chef de Département', 'Chef de Département'), ('Chef de Service', 'Chef de Service'), ('Administrateur de la commune', 'Administrateur de la commune'), ('Chef de Zone', 'Chef de Zone'), ('Chef de Quartier', 'Chef de Quartier')], max_length=250, null=True, verbose_name='Title')),
                ('commune', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='mod_parametrage.commune', verbose_name='Commune')),
                ('departement', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='mod_parametrage.departement', verbose_name='Département')),
                ('quartier', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='mod_parametrage.quartier', verbose_name='Quartier')),
                ('service', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='mod_parametrage.service', verbose_name='Service')),
                ('zone', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='mod_parametrage.zone', verbose_name='Zone')),
            ],
            options={
                'ordering': ('-id',),
            },
        ),
    ]
