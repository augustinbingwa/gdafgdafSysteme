from django.db import models
from django.conf import settings  # authetification user model
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone

from mod_documents.submodels import *

from mod_crm.models import Contribuable
from mod_finance.submodels.model_imposition import path_bordereau_ai_file
from mod_finance.submodels.model_taxe import Taxe

from mod_helpers.hlp_paths import PathsHelpers

from mod_parametrage.enums import *

from decimal import Decimal

import datetime

import pytz


# ----------------------------------------------------------------------------
# ------------------------ GESTION DES DOCUMENTS --------------------
# ----------------------------------------------------------------------------

def path_file_authorisation(instance, filename):
    return PathsHelpers.path_and_rename(instance, filename, PathsHelpers.FOLDER_FILE_AUTHORIZATION)

class NonRedevabilite(models.Model):

    objects = None
    reference = models.CharField(max_length=25, blank=False, unique=True)
    contribuable = models.ForeignKey(Contribuable, on_delete=models.CASCADE, blank=True, null=True)
    nombre_copie = models.PositiveSmallIntegerField(default=1)
    validite = models.PositiveSmallIntegerField(default=1)
    libelle = models.TextField(max_length=512, blank=False)
    fichier_authorization = models.FileField(upload_to=path_file_authorisation, null=True)

    date_create = models.DateTimeField(auto_now_add=True)
    date_update = models.DateTimeField(null=True)  # Mis à jour à chaque modification
    date_validate = models.DateTimeField(null=True)  # Mis à jour à partir du rapprochement
    date_print = models.DateTimeField(null=True)  # Mise à jour après impression

    user_create = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,related_name='%(class)s_requests_created')
    user_update = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,related_name='%(class)s_requests_updated', null=True)
    user_validate = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,related_name='%(class)s_requests_validate', null=True)
    user_print = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,related_name='%(class)s_requests_print', null=True)

    note = models.CharField(max_length=255, blank=True, null=True)
    user_note = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='%(class)s_requests_note', null=True)
    date_note = models.DateTimeField(null=True)

    # Réponse de la note par l'user de création
    reponse_note = models.CharField(max_length=255, blank=True, null=True)

    # Demande d'annulation de validation par l'user de création (Si c'est déjà vadidé)
    demande_annulation_validation = models.BooleanField(default=False)

    # Traçabilité de l'annulation
    date_cancel = models.DateTimeField(null=True)
    user_cancel = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,related_name='%(class)s_requests_cancel', null=True)


    class Meta:
        ordering = ('-id',)

    def __str__(self):
        return self.reference

    def class_name(self):
        """utilisé pour la note : renvoie le path complet de la classe module_._..._.ClasseName """
        return self.__module__ + '.' + self.__class__.__name__



