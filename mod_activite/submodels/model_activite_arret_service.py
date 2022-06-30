from django.conf import settings
from django.db import models
from mod_helpers.hlp_paths import PathsHelpers
from mod_activite.submodels.model_activite import BaseActivite
from django.utils import timezone
import datetime

def path_fichier_formulaire_arret(instance, filename):
    return PathsHelpers.path_and_rename(instance, filename, PathsHelpers.FORMULAIRE_ARRET)

def path_fichier_carte_arret(instance, filename):
    return PathsHelpers.path_and_rename(instance, filename, PathsHelpers.FORMULAIRE_CARTE_ARRET)

class ArretService(models.Model):
    activite = models.ForeignKey(BaseActivite, on_delete=models.CASCADE)

    motif = models.CharField(max_length=100)  # Motif de la remise ou arrête de service

    fichier_formulaire_arret = models.FileField(upload_to=path_fichier_formulaire_arret, max_length=255, null=True, blank=True)  # Un formulaire d'arrêt d'activité à remplir mannuellement et à joindre,
    fichier_carte_arret = models.FileField(upload_to=path_fichier_carte_arret, max_length=255, null=True, blank=True)

    # Traçabilité
    date_arret = models.DateTimeField(null=True)
    user_arret = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='%(class)s_requests_arret', null=True)

    # -------------------------------------------------------
    # ------------------- NOTE ET REPONSE -------------------
    # -------------------------------------------------------
    # Note envoyée par un autre user ou lui mêmes
    note = models.CharField(max_length=255, blank=True, null=True)
    user_note = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='%(class)s_requests_note', null=True)
    date_note = models.DateTimeField(null=True)

    # Réponse de la note par l'user de création
    reponse_note = models.CharField(max_length=255, blank=True, null=True)

    # Demande d'annulation de validation par l'user de création (Si c'est déjà vadidé)
    demande_annulation_validation = models.BooleanField(default=False)

    date_update = models.DateTimeField(null=True)
    user_update = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='%(class)s_requests_updated', null=True)

    date_create = models.DateTimeField(auto_now_add=True)
    user_create = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='%(class)s_requests_created')

    # Traçabilité de l'annulation
    date_cancel = models.DateTimeField(null=True)
    user_cancel = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='%(class)s_requests_cancel', null=True)

    class Meta:
        ordering = ('-id',)

    def __str__(self):
        return self.numero_activite

    def class_name(self):
        """utilisé pour la note : renvoie le path complet de la classe module_._..._.ClasseName """
        return self.__module__ + '.' + self.__class__.__name__

    def view_list_name(self):
        """utilisé pour la note"""
        return 'activite_arret_service_list'