# -------------------------------------------------------------
# -----------------Avis d'Imposition Templates-----------------
# -------------------------------------------------------------

#Avis d'imposition
class AvisImpositionTemplate():
    #CRUD
    index = 'avis_imposition/avis_imposition_list.html'
    list = 'avis_imposition/includes/_avis_imposition_list.html'
    create = 'avis_imposition/includes/_avis_imposition_create.html'
    update = 'avis_imposition/includes/_avis_imposition_update.html'
    delete = 'avis_imposition/includes/_avis_imposition_delete.html'

    #Suivi de paiement
    paiement = 'avis_imposition/includes/_avis_imposition_update_paiement.html'

    #Uploade file
    upload = 'avis_imposition/includes/_avis_imposition_upload.html'

# --------------------------------------------------------------
# -----------------Notes d'Imposition Templates-----------------
# --------------------------------------------------------------

#Note d'imposition Activite Standard
class NI_ActviteStandardTemplate():
    index = 'ni_activite_standard/ni_activite_standard_list.html'
    list = 'ni_activite_standard/includes/_ni_activite_standard_list.html'
    create = 'ni_activite_standard/includes/_ni_activite_standard_create.html'
    update = 'ni_activite_standard/includes/_ni_activite_standard_update.html'

#Note d'imposition Activite Marché
class NI_ActviteMarcheTemplate():
    index = 'ni_activite_marche/ni_activite_marche_list.html'
    list = 'ni_activite_marche/includes/_ni_activite_marche_list.html'
    create = 'ni_activite_marche/includes/_ni_activite_marche_create.html'
    update = 'ni_activite_marche/includes/_ni_activite_marche_update.html'

#Note d'imposition Allocation Place Marché
class NI_AllocationPlaceMarcheTemplate():
    index = 'ni_allocation_place_marche/ni_allocation_place_marche_list.html'
    list = 'ni_allocation_place_marche/includes/_ni_allocation_place_marche_list.html'
    create = 'ni_allocation_place_marche/includes/_ni_allocation_place_marche_create.html'
    update = 'ni_allocation_place_marche/includes/_ni_allocation_place_marche_update.html'

#Note d'imposition Allocation Espace Publique
class NI_AllocationEspacePubliqueTemplate():
    index = 'ni_allocation_espace_publique/ni_allocation_espace_publique_list.html'
    list = 'ni_allocation_espace_publique/includes/_ni_allocation_espace_publique_list.html'
    create = 'ni_allocation_espace_publique/includes/_ni_allocation_espace_publique_create.html'
    update = 'ni_allocation_espace_publique/includes/_ni_allocation_espace_publique_update.html'

#Note d'imposition Allocation Panneau PUblicitaire
class NI_AllocationPanneauPublicitaireTemplate():
    index = 'ni_allocation_panneau_publicitaire/ni_allocation_panneau_publicitaire_list.html'
    list = 'ni_allocation_panneau_publicitaire/includes/_ni_allocation_panneau_publicitaire_list.html'
    create = 'ni_allocation_panneau_publicitaire/includes/_ni_allocation_panneau_publicitaire_create.html'
    update = 'ni_allocation_panneau_publicitaire/includes/_ni_allocation_panneau_publicitaire_update.html'

#Note d'imposition Publicite Mur Cloture
class NI_PubliciteMurClotureTemplate():
    index = 'ni_publicite_mur_cloture/ni_publicite_mur_cloture_list.html'
    list = 'ni_publicite_mur_cloture/includes/_ni_publicite_mur_cloture_list.html'
    create = 'ni_publicite_mur_cloture/includes/_ni_publicite_mur_cloture_create.html'
    update = 'ni_publicite_mur_cloture/includes/_ni_publicite_mur_cloture_update.html'

#Note d'imposition d'activité de transport
class NI_VehiculeActiviteFormTemplate():
    index = 'ni_vehicule_activite/ni_vehicule_activite_list.html'
    list = 'ni_vehicule_activite/includes/_ni_vehicule_activite_list.html'
    create = 'ni_vehicule_activite/includes/_ni_vehicule_activite_create.html'
    update = 'ni_vehicule_activite/includes/_ni_vehicule_activite_update.html'
    upload_externe = 'ni_vehicule_activite/includes/_ni_vehicule_activite_upload_externe.html'

#Note d'imposition de droit de stationnement
class NI_DroitStationnementTemplate():
    index = 'ni_droit_stationnement/ni_droit_stationnement_list.html'
    list = 'ni_droit_stationnement/includes/_ni_droit_stationnement_list.html'
    create = 'ni_droit_stationnement/includes/_ni_droit_stationnement_create.html'
    update = 'ni_droit_stationnement/includes/_ni_droit_stationnement_update.html'

    # PRINT QUITTANCE ERROR
    quittance_print_error = 'ni_droit_stationnement/includes/_ni_droit_stationnement_quittance_print_error.html'

#Note d'imposition impôt sur les titres de propriété
class NI_VehiculeProprietaireTemplate():
    index = 'ni_vehicule_proprietaire/ni_vehicule_proprietaire_list.html'
    list = 'ni_vehicule_proprietaire/includes/_ni_vehicule_proprietaire_list.html'
    create = 'ni_vehicule_proprietaire/includes/_ni_vehicule_proprietaire_create.html'
    update = 'ni_vehicule_proprietaire/includes/_ni_vehicule_proprietaire_update.html'


#Note d'imposition impôt sur les impôts fonciers
class NI_ImpotFoncierTemplate():
    index = 'ni_impot_foncier/ni_impot_foncier_list.html'
    list = 'ni_impot_foncier/includes/_ni_impot_foncier_list.html'
    update = 'ni_impot_foncier/includes/_ni_impot_foncier_update.html'
    changer = 'ni_impot_foncier/includes/_ni_impot_foncier_change_numebord.html'

# --------------------------------------------------------------
# ------------Paiement de Notes d'Imposition Templates----------
# --------------------------------------------------------------

#Paiement note d'imposition
class NoteImpositionPaiementTemplate():
    #CRUD
    index = 'note_imposition_paiement/note_imposition_paiement_list.html'
    list = 'note_imposition_paiement/includes/_note_imposition_paiement_list.html'
    create = 'note_imposition_paiement/includes/_note_imposition_paiement_create.html'
    update = 'note_imposition_paiement/includes/_note_imposition_paiement_update.html'
    delete = 'note_imposition_paiement/includes/_note_imposition_paiement_delete.html'

    #Uploade file
    upload = 'note_imposition_paiement/includes/_note_imposition_paiement_upload.html'

# --------------------------------------------------------------
# -- Demande d'autorization Print Notes d'Imposition Templates -
# --------------------------------------------------------------

#Note d'imposition Print
class NoteImpositionPrintTemplate():
    print = 'note_imposition_print/ni_quittance_print.html'
    print_authorization = 'note_imposition_print/ni_quittance_print_authorization.html'

# --------------------------------------------------------------
# ---------------------- QUITTANCE ERROR -----------------------
# --------------------------------------------------------------
class NI_QuittancePrintErrorTemplate():
    error = 'note_imposition_print/ni_quittance_print_error.html'