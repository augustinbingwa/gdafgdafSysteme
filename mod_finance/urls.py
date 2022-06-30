from django.conf.urls import url

from django.contrib.auth.views import LoginView
from gdaf.forms import LoginForm
 
from mod_finance.views import *

urlpatterns = [

	#-----------------------------------------------------
	#---------- CRUD AVIS D'IMPOSITION -------------------
	#-----------------------------------------------------
	
	#Avis d'imposition CRUD 
	url(r'^finance/avis_imposition/(?P<taxe_filter>\d+)/$', avis_imposition_list, name='avis_imposition_list'),
	url(r'^finance/avis_imposition/create/$', avis_imposition_create, name='avis_imposition_create'),
	url(r'^finance/avis_imposition/(?P<pk>\d+)/update/$', avis_imposition_update, name='avis_imposition_update'),
	url(r'^finance/avis_imposition/(?P<pk>\d+)/delete/$', avis_imposition_delete, name='avis_imposition_delete'),
	
	#Avis d'imposition Validate
	url(r'^finance/avis_imposition/validate/$', avis_imposition_validate, name='avis_imposition_validate'),
	
	#Avis d'imposition Print
	url(r'^finance/avis_imposition/(?P<pk>\d+)/print/$', avis_imposition_print, name='avis_imposition_print'),
	url(r'^finance/avis_imposition_quittance/(?P<pk>\d+)/print/$', avis_imposition_quittance_print, name='avis_imposition_quittance_print'),

	#Avis d'imposition Paiement
	url(r'^finance/avis_imposition/(?P<pk>\d+)/update_paiement/$', avis_imposition_update_paiement, name='avis_imposition_update_paiement'),
	
	#Avis d'imposition Upload
	url(r'^finance/avis_imposition/(?P<pk>\d+)/upload/$', avis_imposition_upload, name='avis_imposition_upload'),

	#-----------------------------------------------------
	#---------- CRUD NOTES D'IMPOSITION ------------------
	#-----------------------------------------------------

	#Note d'imposition CRUD (Activité Standard) 
	url(r'^finance/note_imposition/activite/standard/$', ni_activite_standard_list, name='ni_activite_standard_list'),
	url(r'^finance/note_imposition/activite/standard/(?P<entity_id>\d+)/create/$', ni_activite_standard_create, name='ni_activite_standard_create'),
	url(r'^finance/note_imposition/activite/standard/(?P<pk>\d+)/update/$', ni_activite_standard_update, name='ni_activite_standard_update'),
	url(r'^finance/note_imposition/activite/standard/validate/$', ni_activite_standard_validate, name='ni_activite_standard_validate'),

	#-----------------------------------------------------
	#Note d'imposition CRUD (Activité Marche) 
	url(r'^finance/note_imposition/activite/marche/$', ni_activite_marche_list, name='ni_activite_marche_list'),
	url(r'^finance/note_imposition/activite/marche/(?P<entity_id>\d+)/create/$', ni_activite_marche_create, name='ni_activite_marche_create'),
	url(r'^finance/note_imposition/activite/marche/(?P<pk>\d+)/update/$', ni_activite_marche_update, name='ni_activite_marche_update'),
	url(r'^finance/note_imposition/activite/marche/validate/$', ni_activite_marche_validate, name='ni_activite_marche_validate'),
	
	#-----------------------------------------------------
	#Note d'imposition CRUD (Allocation Place Marche) 
	url(r'^finance/note_imposition/marche_place/allocation/$', ni_allocation_place_marche_list, name='ni_allocation_place_marche_list'),
	url(r'^finance/note_imposition/marche_place/allocation/(?P<entity_id>\d+)/create/$', ni_allocation_place_marche_create, name='ni_allocation_place_marche_create'),
	url(r'^finance/note_imposition/marche_place/allocation/(?P<pk>\d+)/update/$', ni_allocation_place_marche_update, name='ni_allocation_place_marche_update'),
	url(r'^finance/note_imposition/marche_place/allocation/validate/$', ni_allocation_place_marche_validate, name='ni_allocation_place_marche_validate'),
	
	#Note d'imposition CRUD (Allocation Espace Publique) 
	url(r'^finance/note_imposition/espace_publique/allocation/$', ni_allocation_espace_publique_list, name='ni_allocation_espace_publique_list'),
	url(r'^finance/note_imposition/espace_publique/allocation/(?P<entity_id>\d+)/create/$', ni_allocation_espace_publique_create, name='ni_allocation_espace_publique_create'),
	url(r'^finance/note_imposition/espace_publique/allocation/(?P<pk>\d+)/update/$', ni_allocation_espace_publique_update, name='ni_allocation_espace_publique_update'),
	url(r'^finance/note_imposition/espace_publique/allocation/validate/$', ni_allocation_espace_publique_validate, name='ni_allocation_espace_publique_validate'),
	
	#Note d'imposition CRUD (Allocation Panneau Publicitaire) 
	url(r'^finance/note_imposition/panneau_publicitaire/allocation/$', ni_allocation_panneau_publicitaire_list, name='ni_allocation_panneau_publicitaire_list'),
	url(r'^finance/note_imposition/panneau_publicitaire/allocation/(?P<entity_id>\d+)/create/$', ni_allocation_panneau_publicitaire_create, name='ni_allocation_panneau_publicitaire_create'),
	url(r'^finance/note_imposition/panneau_publicitaire/allocation/(?P<pk>\d+)/update/$', ni_allocation_panneau_publicitaire_update, name='ni_allocation_panneau_publicitaire_update'),
	url(r'^finance/note_imposition/panneau_publicitaire/allocation/validate/$', ni_allocation_panneau_publicitaire_validate, name='ni_allocation_panneau_publicitaire_validate'),
	
	#Note d'imposition CRUD (Publicite Mur Cloture) 
	url(r'^finance/note_imposition/publicite/mur_cloture/$', ni_publicite_mur_cloture_list, name='ni_publicite_mur_cloture_list'),
	url(r'^finance/note_imposition/publicite/mur_cloture/(?P<entity_id>\d+)/create/$', ni_publicite_mur_cloture_create, name='ni_publicite_mur_cloture_create'),
	url(r'^finance/note_imposition/publicite/mur_cloture/(?P<pk>\d+)/update/$', ni_publicite_mur_cloture_update, name='ni_publicite_mur_cloture_update'),
	url(r'^finance/note_imposition/publicite/mur_cloture/validate/$', ni_publicite_mur_cloture_validate, name='ni_publicite_mur_cloture_validate'),
	
	#-----------------------------------------------------
	#Note d'imposition CRUD (Transport Activité municipale) 
	url(r'^finance/note_imposition/transport/activite/$', ni_vehicule_activite_list, name='ni_vehicule_activite_list'),
	url(r'^finance/note_imposition/transport/activite/(?P<entity_id>\d+)/create/$', ni_vehicule_activite_create, name='ni_vehicule_activite_create'),
	url(r'^finance/note_imposition/transport/activite/(?P<pk>\d+)/update/$', ni_vehicule_activite_update, name='ni_vehicule_activite_update'),
	url(r'^finance/note_imposition/transport/activite/validate/$', ni_vehicule_activite_validate, name='ni_vehicule_activite_validate'),

	# Upload file : Carte municipale EXTERNE
	url(r'^finance/note_imposition/transport/activite/(?P<pk>\d+)/upload_externe/$', ni_vehicule_activite_externe_upload, name='ni_vehicule_activite_externe_upload'),
	

	#-----------------------------------------------------
	#Note d'imposition CRUD (Transport Droit de stationnement) 
	url(r'^finance/note_imposition/transport/stationnement/$', ni_droit_stationnement_list, name='ni_droit_stationnement_list'),
	url(r'^finance/note_imposition/transport/stationnement/(?P<entity_id>\d+)/create/$', ni_droit_stationnement_create, name='ni_droit_stationnement_create'),
	url(r'^finance/note_imposition/transport/stationnement/(?P<pk>\d+)/update/$', ni_droit_stationnement_update, name='ni_droit_stationnement_update'),
	url(r'^finance/note_imposition/transport/stationnement/validate/$', ni_droit_stationnement_validate, name='ni_droit_stationnement_validate'),
	
	# Impression de la quittance ERROR : Droit de stationnment
	url(r'^finance/note_imposition/transport/stationnement/(?P<pk>\d+)/quittance/print/error/$', ni_droit_stationnement_quittance_print_error, name='ni_droit_stationnement_quittance_print_error'),


	#-----------------------------------------------------
	#Note d'imposition CRUD (Transport Taxe sur les propriétaires) 
	url(r'^finance/note_imposition/transport/proprietaire/$', ni_vehicule_proprietaire_list, name='ni_vehicule_proprietaire_list'),
	url(r'^finance/note_imposition/transport/proprietaire/(?P<entity_id>\d+)/create/$', ni_vehicule_proprietaire_create, name='ni_vehicule_proprietaire_create'),
	url(r'^finance/note_imposition/transport/proprietaire/(?P<pk>\d+)/update/$', ni_vehicule_proprietaire_update, name='ni_vehicule_proprietaire_update'),
	url(r'^finance/note_imposition/transport/proprietaire/validate/$', ni_vehicule_proprietaire_validate, name='ni_vehicule_proprietaire_validate'),

	#-----------------------------------------------------
	#Note d'imposition CRUD (Impôt foncier) 
	url(r'^finance/note_imposition/impot_foncier/$', ni_impot_foncier_list, name='ni_impot_foncier_list'),
	url(r'^finance/note_imposition/impot_foncier/(?P<pk>\d+)/update/$', ni_impot_foncier_update, name='ni_impot_foncier_update'),
	url(r'^finance/note_imposition/impot_foncier/(?P<pk>\d+)/authorisation/$', ni_impot_foncier_authorisation, name='ni_impot_foncier_authorisation'),
	url(r'^finance/note_imposition/impot_foncier/(?P<pk>\d+)/authorisationas/$', ni_impot_foncier_authorisationas, name='ni_impot_foncier_authorisationas'),
	url(r'^finance/note_imposition/impot_foncier/changebordereau/$', ni_impot_foncier_change_numebord, name='ni_impot_foncier_change_numebord'),
	url(r'^finance/note_imposition/num_bordereau/autocomplete/$', numero_bordereau_autocomplete, name='numero_bordereau_autocomplete'),
	
	#-----------------------------------------------------
	#----- PRINT NOTES ET QUITTANCES D'IMPOSITION --------
	#-----------------------------------------------------
	# Impresion de la note
	url(r'^finance/note_imposition/note/(?P<pk>\d+)/print/$', ni_print_pdf, name='ni_print_pdf'),


	# Impression de la quittance
	url(r'^finance/note_imposition/quittance/(?P<pk>\d+)/print/$', ni_quittance_print, name='ni_quittance_print'),
	url(r'^finance/note_imposition/quittance/(?P<pk>\d+)/print/confirm/$', ni_quittance_print_confirm, name='ni_quittance_print_confirm'),
	url(r'^finance/note_imposition/quittance/(?P<pk>\d+)/print/pdf/$', ni_quittance_print_pdf, name='ni_quittance_print_pdf'),
	url(r'^finance/note_imposition/(?P<pk>\d+)/print/authorization/$', ni_quittance_print_authorization, name='ni_quittance_print_authorization'),

	#-----------------------------------------------------
	#---------- PAIEMENT DES NOTES D'IMPOSITION ----------
	#-----------------------------------------------------

	#Paiement note d'imposition CRUD (pk = identifiant de la note)
	url(r'^finance/note_imposition/paiement/(?P<pk>\d+)/$', note_imposition_paiement_list, name='note_imposition_paiement_list'),
	url(r'^finance/note_imposition/paiement/create/$', note_imposition_paiement_create, name='note_imposition_paiement_create'),
	
	#pk = identifiant du paiement de la note
	url(r'^finance/note_imposition/paiement/(?P<pk>\d+)/update/$', note_imposition_paiement_update, name='note_imposition_paiement_update'),
	url(r'^finance/note_imposition/paiement/(?P<pk>\d+)/delete/$', note_imposition_paiement_delete, name='note_imposition_paiement_delete'),
	
	#Paiement note d'imposition : Upload file
	url(r'^finance/note_imposition/paiement/(?P<pk>\d+)/upload/$', note_imposition_paiement_upload, name='note_imposition_paiement_upload'),
	url(r'^finance/note_imposition/paiement/(?P<pk>\d+)/upload_temp/$', note_imposition_paiement_upload_temp, name='note_imposition_paiement_upload_temp'),

	#paiement de la note d'imposition : validate details paiement
	url(r'^finance/note_imposition/paiement/(?P<pk>\d+)/validate/$', note_imposition_paiement_validate, name='note_imposition_paiement_validate'),

	#-----------------------------------------------------
	#------------------- HELPERS -------------------------
	#-----------------------------------------------------
	
	url(r'^finance/taxe_activite/autocomplete/$', taxe_activite_autocomplete, name='taxe_activite_autocomplete'),

	#Avis d'imposition non utilisé (non attaché ou non attribué)
	url(r'^finance/avis_imposition_unused/autocomplete/(?P<taxe_filter>\d+)/$', avis_imposition_unused_autocomplete, name='avis_imposition_unused_autocomplete'),

	#Avis d'imposition taxe changed
	url(r'^finance/avis_imposition/helpers/taxe_changed/$', avis_imposition_taxe_changed, name='avis_imposition_taxe_changed'),

	#Note d'imposition non utilisés (non attachés ou non attribués)
	url(r'^finance/note_imposition_unused/autocomplete/$', note_imposition_unused_autocomplete, name='note_imposition_unused_autocomplete'),

	#Note d'imposition taxe changed
	url(r'^finance/note_imposition/helpers/taxe_changed/$', note_imposition_taxe_changed, name='note_imposition_taxe_changed'),


	#-----------------------------------------------------
	#--------- LOGOUT/LOGIN URL !!! IMPORTANT !!! --------
	#-----------------------------------------------------  
	url(r'^finance/avis_imposition/login/$', LoginView.as_view(), {'template_name': 'login.html', 'authentication_form': LoginForm}, name='login'),
	url(r'^finance/note_imposition/activite/standard/login/$', LoginView.as_view(), {'template_name': 'login.html', 'authentication_form': LoginForm}, name='login'),
	url(r'^finance/note_imposition/activite/marche/login/$', LoginView.as_view(), {'template_name': 'login.html', 'authentication_form': LoginForm}, name='login'),
	url(r'^finance/note_imposition/marche_place/allocation/login/$', LoginView.as_view(), {'template_name': 'login.html', 'authentication_form': LoginForm}, name='login'),
	url(r'^finance/note_imposition/espace_publique/allocation/login/$', LoginView.as_view(), {'template_name': 'login.html', 'authentication_form': LoginForm}, name='login'),
	url(r'^finance/note_imposition/panneau_publicitaire/allocation/login/$', LoginView.as_view(), {'template_name': 'login.html', 'authentication_form': LoginForm}, name='login'),
	url(r'^finance/note_imposition/publicite/mur_cloture/login/$', LoginView.as_view(), {'template_name': 'login.html', 'authentication_form': LoginForm}, name='login'),
	url(r'^finance/note_imposition/transport/activite/login/$', LoginView.as_view(), {'template_name': 'login.html', 'authentication_form': LoginForm}, name='login'),
	url(r'^finance/note_imposition/transport/stationnement/login/$', LoginView.as_view(), {'template_name': 'login.html', 'authentication_form': LoginForm}, name='login'),
	url(r'^finance/note_imposition/transport/proprietaire/login/$', LoginView.as_view(), {'template_name': 'login.html', 'authentication_form': LoginForm}, name='login'),
	url(r'^finance/note_imposition/impot_foncier/login/$',LoginView.as_view(), {'template_name': 'login.html', 'authentication_form': LoginForm}, name='login'),
	url(r'^finance/note_imposition/paiement/login/$', LoginView.as_view(), {'template_name': 'login.html', 'authentication_form': LoginForm}, name='login'),
	url(r'^finance/note_imposition/paiement/(?P<pk>\d+)/login/$', LoginView.as_view(), {'template_name': 'login.html', 'authentication_form': LoginForm}, name='login'),
	url(r'^finance/note_imposition/note/login/$', LoginView.as_view(), {'template_name': 'login.html', 'authentication_form': LoginForm}, name='login'),
	url(r'^finance/note_imposition/quittance/login/$', LoginView.as_view(), {'template_name': 'login.html', 'authentication_form': LoginForm}, name='login'),

]