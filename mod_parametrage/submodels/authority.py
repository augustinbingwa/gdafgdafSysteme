from django.db import models
from .fonction import Fonction


class Authority(models.Model):
    nom = models.CharField(max_length=20)
    prenom = models.CharField(max_length=20)
    fonction = models.ForeignKey(Fonction, on_delete=models.CASCADE)
    actif = models.BooleanField(default=True)
    class Meta:
        ordering = ('-id',)

    def __str__(self):
        return self.nom+' '+self.prenom