from django.conf import settings
from django.db import models
from .adresse import *

class Fonction(models.Model):
    LOCALITE = (
        ('MR', 'Mairie'),
        ('DP', 'Département'),
        ('SR', 'Service'),
        ('CM', 'Commune'),
        ('ZN', 'Zone'),
        ('QT', 'Quartier'),
    )
    TITLE = (
        ('Maire de la ville', 'Maire de la ville'),
        ('Chef de Département', 'Chef de Département'),
        ('Chef de Service', 'Chef de Service'),
        ('Administrateur de la commune', 'Administrateur de la commune'),
        ('Chef de Zone', 'Chef de Zone'),
        ('Chef de Quartier', 'Chef de Quartier'),
    )

    libele = models.CharField(max_length=250,choices=LOCALITE,null=True,blank=True,verbose_name="Localité")
    title = models.CharField(max_length=250,choices=TITLE,null=True,blank=True,verbose_name="Title")
    departement = models.ForeignKey(Departement, on_delete=models.CASCADE,null=True,blank=True,verbose_name="Département")
    service = models.ForeignKey(Service, on_delete=models.CASCADE,null=True,blank=True,verbose_name="Service")
    commune = models.ForeignKey(Commune, on_delete=models.CASCADE,null=True,blank=True,verbose_name="Commune")
    zone = models.ForeignKey(Zone, on_delete=models.CASCADE,null=True,blank=True,verbose_name="Zone")
    quartier = models.ForeignKey(Quartier, on_delete=models.CASCADE,null=True,blank=True,verbose_name="Quartier")

    class Meta:
        ordering = ('-id',)

    def __str__(self):
        if not self.departement:
            departement = ''
        else:
            departement = str(self.departement)

        if not self.service:
            service = ''
        else:
            service = str(self.service)

        if not self.commune:
            commune = ''
        else:
            commune = str(self.commune)

        if not self.zone:
            zone = ''
        else:
            zone = str(self.zone)

        if not self.quartier:
            quartier = ''
        else:
            quartier = str(self.quartier)


        return self.title + ' ' + departement + ' '+ service + ' ' + commune + ' ' + zone + ' ' + quartier