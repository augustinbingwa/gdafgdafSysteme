from django.conf import settings #authetification user model
from django.db import models
from mod_crm.models import Contribuable
from django.core.validators import MinValueValidator
from mod_finance.models import Agence
from decimal import Decimal


class CompteContribuable(models.Model):
    """
    Modele Compte de Contribuable.
    """
    description = models.CharField(max_length=250)
    contribuable = models.ForeignKey(Contribuable, on_delete=models.CASCADE)
    agence = models.ForeignKey(Agence, on_delete=models.CASCADE)
    ref_paiement = models.CharField(max_length=50)  # référence de paiement (ref boredereau)
    date_paiement = models.DateTimeField()
    # Montant tranche payé
    Solde = models.DecimalField(decimal_places=2, max_digits=10, validators=[MinValueValidator(Decimal('0'))])
    # Traçabilité
    date_create = models.DateTimeField(auto_now_add=True)
    date_update = models.DateTimeField(null=True)
    user_create = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,related_name='%(class)s_requests_created')
    user_update = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,related_name='%(class)s_requests_updated', null=True)

    class Meta:
        ordering = ('-id',)

    def __str__(self):
        return self.ref_paiement

