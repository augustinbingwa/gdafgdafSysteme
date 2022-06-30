# Generated by Django 2.0.7 on 2018-11-21 11:09

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('mod_finance', '0048_auto_20181120_1100'),
    ]

    operations = [
        migrations.AddField(
            model_name='noteimpositionpaiement',
            name='date_cancel',
            field=models.DateTimeField(null=True),
        ),
        migrations.AddField(
            model_name='noteimpositionpaiement',
            name='date_note',
            field=models.DateTimeField(null=True),
        ),
        migrations.AddField(
            model_name='noteimpositionpaiement',
            name='demande_annulation_validation',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='noteimpositionpaiement',
            name='note',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='noteimpositionpaiement',
            name='reponse_note',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='noteimpositionpaiement',
            name='user_cancel',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='noteimpositionpaiement_requests_cancel', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='noteimpositionpaiement',
            name='user_note',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='noteimpositionpaiement_requests_note', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='avisimposition',
            name='entity',
            field=models.IntegerField(choices=[(5, 'Django-Model:AllocationEspacePublique'), (2, 'Django-Model:Marche'), (4, 'Django-Model:VisiteSiteTouristique'), (16, 'Django-Model:VehiculeActiviteDuplicata'), (12, 'Django-Model:VehiculeActivite'), (7, 'Django-Model:PubliciteMurCloture'), (8, 'Django-Model:AllocationPlaceMarche'), (14, 'Django-Model:BaseActiviteDuplicata'), (1, 'Django-Model:Standard'), (17, 'Django-Model:VehiculeProprietaireDuplicata'), (18, 'Django-Model:BetailsPropriete'), (9, 'Location batiments municipaux'), (10, 'Django-Model:FoncierParcelle'), (15, 'Django-Model:FoncierParcelleDuplicata'), (13, 'Django-Model:VehiculeProprietaire'), (6, 'Django-Model:AllocationPanneauPublicitaire'), (3, 'Django-Model:ActiviteExceptionnel'), (11, 'Django-Model:VehiculeActivite')], null=True),
        ),
        migrations.AlterField(
            model_name='noteimposition',
            name='entity',
            field=models.IntegerField(choices=[(5, 'Django-Model:AllocationEspacePublique'), (2, 'Django-Model:Marche'), (4, 'Django-Model:VisiteSiteTouristique'), (16, 'Django-Model:VehiculeActiviteDuplicata'), (12, 'Django-Model:VehiculeActivite'), (7, 'Django-Model:PubliciteMurCloture'), (8, 'Django-Model:AllocationPlaceMarche'), (14, 'Django-Model:BaseActiviteDuplicata'), (1, 'Django-Model:Standard'), (17, 'Django-Model:VehiculeProprietaireDuplicata'), (18, 'Django-Model:BetailsPropriete'), (9, 'Location batiments municipaux'), (10, 'Django-Model:FoncierParcelle'), (15, 'Django-Model:FoncierParcelleDuplicata'), (13, 'Django-Model:VehiculeProprietaire'), (6, 'Django-Model:AllocationPanneauPublicitaire'), (3, 'Django-Model:ActiviteExceptionnel'), (11, 'Django-Model:VehiculeActivite')], null=True),
        ),
        migrations.AlterField(
            model_name='periode',
            name='element',
            field=models.IntegerField(choices=[(3, 'Mars'), (8, 'Août'), (16, '4e Trimestre'), (10, 'Octobre'), (15, '3e Trimestre'), (4, 'Avril'), (6, 'Juin'), (1, 'Janvier'), (7, 'Juillet'), (9, 'Septembre'), (11, 'Novembre'), (12, 'Décembre'), (13, '1er Trimestre'), (18, '2e Semestre'), (5, 'Mai'), (17, '1er Semestre'), (14, '2e Trimestre'), (19, 'Année'), (2, 'Février')], verbose_name='Elements de période'),
        ),
        migrations.AlterField(
            model_name='periodetype',
            name='categorie',
            field=models.IntegerField(choices=[(4, 'Annuelle'), (0, 'Autre'), (2, 'Trimestrielle'), (1, 'Mensuelle'), (3, 'Semestrielle')], default=0, verbose_name='catégorie de périodes'),
        ),
    ]
