# Generated by Django 2.0.7 on 2019-02-20 15:10

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('mod_finance', '0106_auto_20190220_1255'),
    ]

    operations = [
        migrations.AddField(
            model_name='noteimposition',
            name='date_delete',
            field=models.DateTimeField(null=True),
        ),
        migrations.AddField(
            model_name='noteimposition',
            name='motif_delete',
            field=models.TextField(blank=True, max_length=1024, null=True),
        ),
        migrations.AddField(
            model_name='noteimposition',
            name='user_delete',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='noteimposition_requests_delete', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='avisimposition',
            name='entity',
            field=models.IntegerField(choices=[(5, 'Django-Model:AllocationEspacePublique'), (12, 'Django-Model:VehiculeActivite'), (4, 'Django-Model:VisiteSiteTouristique'), (7, 'Django-Model:PubliciteMurCloture'), (11, 'Django-Model:VehiculeActivite'), (16, 'Django-Model:VehiculeActiviteDuplicata'), (13, 'Django-Model:VehiculeProprietaire'), (8, 'Django-Model:AllocationPlaceMarche'), (17, 'Django-Model:VehiculeProprietaireDuplicata'), (3, 'Django-Model:ActiviteExceptionnel'), (10, 'Django-Model:FoncierParcelle'), (1, 'Django-Model:Standard'), (6, 'Django-Model:AllocationPanneauPublicitaire'), (18, 'Django-Model:BetailsPropriete'), (2, 'Django-Model:Marche'), (14, 'Django-Model:BaseActiviteDuplicata'), (9, 'Location batiments municipaux'), (15, 'Django-Model:FoncierParcelleDuplicata')], null=True),
        ),
        migrations.AlterField(
            model_name='noteimposition',
            name='entity',
            field=models.IntegerField(choices=[(5, 'Django-Model:AllocationEspacePublique'), (12, 'Django-Model:VehiculeActivite'), (4, 'Django-Model:VisiteSiteTouristique'), (7, 'Django-Model:PubliciteMurCloture'), (11, 'Django-Model:VehiculeActivite'), (16, 'Django-Model:VehiculeActiviteDuplicata'), (13, 'Django-Model:VehiculeProprietaire'), (8, 'Django-Model:AllocationPlaceMarche'), (17, 'Django-Model:VehiculeProprietaireDuplicata'), (3, 'Django-Model:ActiviteExceptionnel'), (10, 'Django-Model:FoncierParcelle'), (1, 'Django-Model:Standard'), (6, 'Django-Model:AllocationPanneauPublicitaire'), (18, 'Django-Model:BetailsPropriete'), (2, 'Django-Model:Marche'), (14, 'Django-Model:BaseActiviteDuplicata'), (9, 'Location batiments municipaux'), (15, 'Django-Model:FoncierParcelleDuplicata')], null=True),
        ),
        migrations.AlterField(
            model_name='periode',
            name='element',
            field=models.IntegerField(choices=[(12, 'Décembre'), (15, '3e Trimestre'), (13, '1er Trimestre'), (2, 'Février'), (6, 'Juin'), (16, '4e Trimestre'), (7, 'Juillet'), (3, 'Mars'), (10, 'Octobre'), (18, '2e Semestre'), (8, 'Août'), (4, 'Avril'), (17, '1er Semestre'), (5, 'Mai'), (14, '2e Trimestre'), (1, 'Janvier'), (9, 'Septembre'), (19, 'Année'), (11, 'Novembre')], verbose_name='Elements de période'),
        ),
        migrations.AlterField(
            model_name='periodetype',
            name='categorie',
            field=models.IntegerField(choices=[(4, 'Annuelle'), (0, 'Autre'), (2, 'Trimestrielle'), (1, 'Mensuelle'), (3, 'Semestrielle')], default=0, verbose_name='catégorie de périodes'),
        ),
    ]
