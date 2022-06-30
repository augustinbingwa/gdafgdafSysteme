from django.db import models
from django.contrib.auth import get_user_model

from mod_parametrage.enums import *

# We check the user here
User = get_user_model()

# Modele Opérateur. Ex : Banque, Mobile Money...
class Operateur(models.Model):
    libelle = models.CharField(max_length=25, blank=False, unique=True)

    class Meta:
        ordering = ("libelle",)

    def __str__(self):
        return self.libelle


# Modele Agence de paiement : Banque ou Mobile Money
class Agence(models.Model):
    code = models.CharField(max_length=10, blank=False, unique=True)
    sigle = models.CharField(max_length=10, blank=False, unique=True)
    nom = models.CharField(max_length=100, blank=False, unique=True)
    compte = models.CharField(max_length=15, blank=False, unique=True)
    operateur = models.ForeignKey(Operateur, on_delete=models.CASCADE)

    def get_user(self):
        if hasattr(self, "agenceuser"):
            return self.agenceuser

    @classmethod
    def get_for_user(cls, user):
        try:
            return cls.objects.get(bankuser__user=user)
        except cls.DoesNotExist:
            return None

    class Meta:
        ordering = ("code",)

    def __str__(self):
        return self.sigle


class AgenceUser(models.Model):
    agence = models.OneToOneField(
        "Agence",
        on_delete=models.PROTECT,
        related_name="user",
        related_query_name="bankuser",
    )
    user = models.OneToOneField(
        User,
        related_name="agence",
        related_query_name="agenceuser",
        on_delete=models.PROTECT,
    )


# Modele Type de Periode de paiement. Ex : Mensuel, Trimestriel, Semestriel, Annuel, Autre (kg, eplacement, bidon, ...)
class PeriodeType(models.Model):
    libelle = models.CharField(max_length=25, blank=False, unique=True)
    temps = models.BooleanField()  # True, pour les périodes basées sur le temps
    categorie = models.IntegerField(
        choices=choix_periode_categories,
        default=0,
        verbose_name="catégorie de périodes",
    )

    class Meta:
        ordering = ("id",)

    def __str__(self):
        return self.libelle


# Modele Composante période de paiement de la taxe sur activité
class Periode(models.Model):
    periode_type = models.ForeignKey(PeriodeType, on_delete=models.CASCADE)

    # Elemenets de la période Ex : Janvier, Fevrier, ..., 1er Trimestre, 2e Trimestre, Annee, etc.
    element = models.IntegerField(
        choices=choix_periode_elements, verbose_name="Elements de période"
    )

    class Meta:
        ordering = (
            "periode_type",
            "element",
        )

    def __str__(self):
        return u"%s - %s" % (
            self.periode_type.get_categorie_display(),
            self.get_element_display(),
        )
