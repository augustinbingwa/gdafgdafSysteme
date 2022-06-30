# Generated by Django 2.0.7 on 2018-10-29 06:24

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('mod_finance', '0015_auto_20181026_1503'),
    ]

    operations = [
        migrations.AddField(
            model_name='avisimposition',
            name='date_note',
            field=models.DateTimeField(null=True),
        ),
        migrations.AddField(
            model_name='avisimposition',
            name='demande_annulation_validation',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='avisimposition',
            name='reponse_note',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='avisimposition',
            name='user_note',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='avisimposition_requests_note', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='noteimposition',
            name='date_note',
            field=models.DateTimeField(null=True),
        ),
        migrations.AddField(
            model_name='noteimposition',
            name='demande_annulation_validation',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='noteimposition',
            name='reponse_note',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='noteimposition',
            name='user_note',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='noteimposition_requests_note', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='avisimposition',
            name='entity',
            field=models.IntegerField(choices=[(14, 'Django-Model:BaseActiviteDuplicata'), (4, 'Django-Model:VisiteSiteTouristique'), (2, 'Django-Model:Marche'), (9, 'Location batiments municipaux'), (5, 'Django-Model:AllocationEspacePublique'), (11, 'Django-Model:VehiculeActivite'), (13, 'Django-Model:VehiculeProprietaire'), (7, 'Django-Model:PubliciteMurCloture'), (1, 'Django-Model:Standard'), (10, 'Django-Model:FoncierParcelle'), (18, 'Django-Model:BetailsPropriete'), (17, 'Django-Model:VehiculeProprietaireDuplicata'), (12, 'Django-Model:VehiculeActivite'), (16, 'Django-Model:VehiculeActiviteDuplicata'), (6, 'Django-Model:AllocationPanneauPublicitaire'), (15, 'Django-Model:FoncierParcelleDuplicata'), (8, 'Django-Model:AllocationPlaceMarche'), (3, 'Django-Model:ActiviteExceptionnel')], null=True),
        ),
        migrations.AlterField(
            model_name='noteimposition',
            name='entity',
            field=models.IntegerField(choices=[(14, 'Django-Model:BaseActiviteDuplicata'), (4, 'Django-Model:VisiteSiteTouristique'), (2, 'Django-Model:Marche'), (9, 'Location batiments municipaux'), (5, 'Django-Model:AllocationEspacePublique'), (11, 'Django-Model:VehiculeActivite'), (13, 'Django-Model:VehiculeProprietaire'), (7, 'Django-Model:PubliciteMurCloture'), (1, 'Django-Model:Standard'), (10, 'Django-Model:FoncierParcelle'), (18, 'Django-Model:BetailsPropriete'), (17, 'Django-Model:VehiculeProprietaireDuplicata'), (12, 'Django-Model:VehiculeActivite'), (16, 'Django-Model:VehiculeActiviteDuplicata'), (6, 'Django-Model:AllocationPanneauPublicitaire'), (15, 'Django-Model:FoncierParcelleDuplicata'), (8, 'Django-Model:AllocationPlaceMarche'), (3, 'Django-Model:ActiviteExceptionnel')], null=True),
        ),
        migrations.AlterField(
            model_name='periode',
            name='element',
            field=models.IntegerField(choices=[(16, '4e Timestre'), (18, '2e Semestre'), (9, 'Septembre'), (3, 'Mars'), (6, 'Juin'), (7, 'Juillet'), (19, 'Année'), (10, 'Octobre'), (14, '2e Trimestre'), (2, 'Février'), (12, 'Décembre'), (1, 'Janvier'), (11, 'Novembre'), (15, '3e Trimestre'), (4, 'Avril'), (8, 'Août'), (13, '1er Trimestre'), (5, 'Mai'), (17, '1er Semestre')], verbose_name='Elements de période'),
        ),
        migrations.AlterField(
            model_name='periodetype',
            name='categorie',
            field=models.IntegerField(choices=[(0, 'Autre'), (4, 'Annuelle'), (3, 'Semestrielle'), (2, 'Trimestrielle'), (1, 'Mensuelle')], default=0, verbose_name='catégorie de périodes'),
        ),
    ]