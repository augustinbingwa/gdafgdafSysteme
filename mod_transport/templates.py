# ----------------------------------------------------------------------------------
# ------------------Vehicule Templates----------------------------------------------
# ----------------------------------------------------------------------------------
class VehiculeTemplate():
    #Crud
    index = 'vehicule/vehicule_list.html'
    list = 'vehicule/include/_vehicule_list.html'
    create = 'vehicule/include/_vehicule_create.html'
    update = 'vehicule/include/_vehicule_update.html'
    delete = 'vehicule/include/_vehicule_delete.html'

    #Uploade file
    upload = 'vehicule/include/_vehicule_upload.html'

# ----------------------------------------------------------------------------------
# ------------------Vehicule Activité Templates-------------------------------------
# ----------------------------------------------------------------------------------
class VehiculeActiviteTemplate():
    #Crud
    index = 'vehicule_activite/vehicule_activite_list.html'
    list = 'vehicule_activite/include/_vehicule_activite_list.html'
    create = 'vehicule_activite/include/_vehicule_activite_create.html'
    update = 'vehicule_activite/include/_vehicule_activite_update.html'
    delete = 'vehicule_activite/include/_vehicule_activite_delete.html'
    arret = 'vehicule_activite/include/_vehicule_activite_create_arret.html'

    #Uploade file
    upload = 'vehicule_activite/include/_vehicule_activite_upload.html'

    # Print
    print = 'vehicule_activite/include/_vehicule_activite_print.html'
    print_authorization = 'vehicule_activite/include/_vehicule_activite_print_authorization.html'

# ----------------------------------------------------------------------------------
# -----------------Carte Activite Trasport Duplicata Template-----------------------
# ----------------------------------------------------------------------------------
class VehiculeActiviteDuplicataTemplate():
    #Crud
    index = 'vehicule_activite_duplicata/vehicule_activite_duplicata_list.html'
    list = 'vehicule_activite_duplicata/include/_vehicule_activite_duplicata_list.html'
    create = 'vehicule_activite_duplicata/include/_vehicule_activite_duplicata_create.html'
    update = 'vehicule_activite_duplicata/include/_vehicule_activite_duplicata_update.html'
    delete = 'vehicule_activite_duplicata/include/_vehicule_activite_duplicata_delete.html'

    # Print
    print = 'vehicule_activite_duplicata/include/_vehicule_activite_duplicata_print.html'
    print_authorization = 'vehicule_activite_duplicata/include/_vehicule_activite_duplicata_print_authorization.html'

# ----------------------------------------------------------------------------------
# -----------------Véhicule Proprietaire Template-----------------------------------
# ----------------------------------------------------------------------------------
class VehiculeProprietaireTemplate():
    #Crud
    index = 'vehicule_proprietaire/vehicule_proprietaire_list.html'
    list = 'vehicule_proprietaire/include/_vehicule_proprietaire_list.html'
    create = 'vehicule_proprietaire/include/_vehicule_proprietaire_create.html'
    update = 'vehicule_proprietaire/include/_vehicule_proprietaire_update.html'
    delete = 'vehicule_proprietaire/include/_vehicule_proprietaire_delete.html'

    # Print
    print = 'vehicule_proprietaire/include/_vehicule_proprietaire_print.html'
    print_authorization = 'vehicule_proprietaire/include/_vehicule_proprietaire_print_authorization.html'

# ----------------------------------------------------------------------------------
# -----------------Carte Proprietaire Duplicata Template----------------------------
# ----------------------------------------------------------------------------------
class VehiculeProprietaireDuplicataTemplate():
    #Crud
    index = 'vehicule_proprietaire_duplicata/vehicule_proprietaire_duplicata_list.html'
    list = 'vehicule_proprietaire_duplicata/include/_vehicule_proprietaire_duplicata_list.html'
    create = 'vehicule_proprietaire_duplicata/include/_vehicule_proprietaire_duplicata_create.html'
    update = 'vehicule_proprietaire_duplicata/include/_vehicule_proprietaire_duplicata_update.html'
    delete = 'vehicule_proprietaire_duplicata/include/_vehicule_proprietaire_duplicata_delete.html'

    # Print
    print = 'vehicule_proprietaire_duplicata/include/_vehicule_proprietaire_duplicata_print.html'
    print_authorization = 'vehicule_proprietaire_duplicata/include/_vehicule_proprietaire_duplicata_print_authorization.html'

# ----------------------------------------------------------------------------------
# ------------------Vehicule Stationnement Templates--------------------------------
# ----------------------------------------------------------------------------------
class VehiculeStationnementTemplate():
    #Crud
    index = 'vehicule_stationnement/vehicule_stationnement_list.html'
    list = 'vehicule_stationnement/include/_vehicule_stationnement_list.html'



# --------------------------------------------------------
# ----------------- Vehicule arrêt service ---------------
# --------------------------------------------------------
class VehiculeArretServiceTemplate():
    index = 'vehicule_arret_service/vehicule_arret_service_list.html'
    list = 'vehicule_arret_service/includes/_vehicule_arret_service_list.html'
    create = 'vehicule_arret_service/includes/_vehicule_arret_service_create.html'
    update = 'vehicule_arret_service/includes/_vehicule_arret_service_update.html'
    reouverture = 'vehicule_arret_service/includes/_vehicule_reouverture_service.html'
    delete = 'vehicule_arret_service/includes/_vehicule_arret_service_delete.html'
    upload = 'vehicule_arret_service/includes/_vehicule_arret_service_upload.html'
    upload_carte = 'vehicule_arret_service/includes/_vehicule_carte_municipale_upload.html'
    errormassage = '_message_erreur.html'

# --------------------------------------------------------
# ----------------- Vehicule transfert ---------------
# --------------------------------------------------------
class VehiculeTransfertTemplate():
    index = 'vehicule_transfert/vehicule_transfert_list.html'
    list = 'vehicule_transfert/include/_vehicule_transfert_list.html'
    create = 'vehicule_transfert/include/_vehicule_transfert_create.html'
    update = 'vehicule_transfert/include/_vehicule_transfert_update.html'
    upload = 'vehicule_transfert/include/_vehicule_transfert_upload.html'
    delete = 'vehicule_transfert/include/_vehicule_transfert_delete.html'