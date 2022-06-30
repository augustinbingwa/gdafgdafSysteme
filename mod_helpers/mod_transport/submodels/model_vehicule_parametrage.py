from django.db import models

from mod_finance.models import Taxe

from mod_parametrage.enums import *

class VehiculeCategorie(models.Model):
    """
    Modèle Catégorie des véhicules.
    Ex : Véhicules à 4 roues, Véhicules à 3 et à 2 roues (motocyclette/tuk-tuk), Véhicules à
    2 roues (bicyclette/cyclomoteur)
    """
    nom = models.CharField(max_length=50, blank=False, unique=True, verbose_name="Nom de la catégorie des véhicules ")

    #Les voitures à quatre roues ont de différentes plaques (UNIQUE)
    #Les voiture à 2 ou 3 (Moto ou Bajaj) ont de différentes plaques (UNIQUE)
    #Remarque : Les 4 ou 3 ou 2 roues peuvent avoir la même plaque (Exception)
    #Lors de l'ajour d'un véhicule de même catégorie (4 ou 3/2 roues) il faut vérifier l'unicité de plaque
    """
    choix_type_roue = ( 
        (0, 'pas de roue'), #Bateau 
        (1, '2 ou 3 roues'), #Moto - Bajaj - Vélo 
        (2, '4 roues'), #Camion - Voiture - Bus - ... //Ils sont obligatoirement REMUNERE
    )
    """
    type_roue = models.IntegerField(verbose_name="Type de roue", choices=choix_type_roue)

    class Meta:
        ordering = ('nom', 'type_roue',)

    def __str__(self):
        return self.nom

class VehiculeSousCategorie(models.Model):
    """
    Modèle Sous Catégorie des véhicules.
    Ex : Voiture, Motocyclette, Tuk-tuk (Bajaj), Vélo (bicyclete), Cyclomoteur
    """
    nom = models.CharField(max_length=50, blank=False, unique=True, verbose_name="Sous-catégorie")

    categorie = models.ForeignKey(VehiculeCategorie, on_delete=models.CASCADE, verbose_name="Catégorie")

    # Si la voiture est une voiture de trasport commun (=> afficher le nombre de place dans Véhicule)
    transport_commun = models.BooleanField(verbose_name="Si transport commun", default=False)

    # Seules les cyclo et cylomoteur n'ont pas de plaque (Mais on attribue des numéro chrono modifiabe)
    has_plaque = models.BooleanField(verbose_name="Avoir plaque", default=True)

    # Sous Catégorie de Véhicule qui pourrait ne pas exercer des activité municipales (ces véhicules sont des véhicules inter-ubain à compte propre)
    # Mais qui paient regulièrement le droit de stationnement
    has_compte_propre = models.BooleanField(verbose_name="Compte propre (sans activité mais qui paierait seulement le droit de stationnement)", default=False)
    
    # Coût de la carte de propriétaire : (Avis d’imposition)
    ai_cout_carte_propriete = models.ForeignKey(Taxe, on_delete=models.CASCADE, null=True, blank=True,
                                      related_name='%(class)s_requests_taxe_ai_cout_carte_propriete',
                                      verbose_name="Coût de la carte de propriété (AVIS)")

    # Coût de la carte professionnelle : (Avis d’imposition)
    ai_cout_carte_professionnelle = models.ForeignKey(Taxe, on_delete=models.CASCADE, null=True, blank=True,
                                      related_name='%(class)s_requests_taxe_ai_cout_carte_professionnelle',
                                      verbose_name="Coût de la carte professionnelle (AVIS)")

    # Taxe sur activité rémunéré (Note d'imposition)
    taxe_activite = models.ForeignKey(Taxe, on_delete=models.CASCADE, null=True, blank=True,
                                      related_name='%(class)s_requests_taxe_ni_activite', 
                                      verbose_name="Taxe sur activité (NOTE)")

    # Droit de stationnement (Note d'imposition)
    taxe_stationnement = models.ForeignKey(Taxe, on_delete=models.CASCADE, null=True, blank=True,
                                           related_name='%(class)s_requests_taxe_ni_stationnement',
                                           verbose_name="Droit de stationnement (NOTE)")

    # Impôt sur les propriétaires (Note d'imposition)
    taxe_proprietaire = models.ForeignKey(Taxe, on_delete=models.CASCADE, null=True, blank=True,
                                          related_name='%(class)s_requests_taxe_ni_proprietaire',
                                          verbose_name="Taxe sur le propriétaire (NOTE)")
     # Coût duplicata de la carte professionnelle : (Avis d’imposition)
    ai_cout_duplicata_carte_professionnelle = models.ForeignKey(Taxe, on_delete=models.CASCADE, null=True, blank=True,
                                      related_name='%(class)s_requests_taxe_ai_cout_duplicata_carte_professionnelle',
                                      verbose_name="Coût duplicata de la carte professionnelle (AVIS)")
    class Meta:
        ordering = ('categorie',)

    def __str__(self):
        return self.categorie.nom + ' - ' + self.nom

class VehiculeMarque(models.Model):
    """
    Modèle 'Marque du véhicule'
    Ex : Bmw, Audi, Toyota, ...
    """
    nom = models.CharField(max_length=50, blank=False, unique=True, verbose_name="Marque du véhicule")

    class Meta:
        ordering = ('id',)

    def __str__(self):
        return self.nom

class VehiculeModele(models.Model): 
    """
    Modèle 'Modèle du véhicule'
    Ex : Bmw Serie 3, Audi A1, Toyota Carina, ...
    """
    marque = models.ForeignKey(VehiculeMarque, on_delete=models.CASCADE, verbose_name="Marque du véhicule")
    nom = models.CharField(max_length=50, unique=True, blank=False, verbose_name="Modèle du véhicule")

    class Meta:
        ordering = ('nom', )

    def __str__(self):
        return self.nom