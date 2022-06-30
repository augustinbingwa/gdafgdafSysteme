from django.conf.urls import url
from django.contrib.auth.views import LoginView
from gdaf.forms import LoginForm

from .views import * 

urlpatterns = [
	#-----------------------------------------------------
	#---------------- CRUD ACTIVITE STANDARD -------------
	#-----------------------------------------------------	
	url(r'^activite/standard/$', activite_standard_list, name='activite_standard_list'),
	url(r'^activite/standard/create/$', activite_standard_create, name='activite_standard_create'),
	url(r'^activite/standard/(?P<pk>\d+)/update/$', activite_standard_update, name='activite_standard_update'),
	url(r'^activite/standard/(?P<pk>\d+)/delete/$', activite_standard_delete, name='activite_standard_delete'),
	url(r'^activite/standard/(?P<pk>\d+)/upload/$', activite_standard_upload, name='activite_standard_upload'),
	url(r'^activite/standard/validate/$', activite_standard_validate, name='activite_standard_validate'),
	url(r'^activite/standard/ecriture/$', activite_standard_ecriture, name='activite_standard_ecriture'),

	# Print carte activite marché
	url(r'^activite/standard/(?P<pk>\d+)/print/$', activite_standard_print, name='activite_standard_print'),
	url(r'^activite/standard/(?P<pk>\d+)/print/authorization/$', activite_standard_print_authorization, name='activite_standard_print_authorization'),
	url(r'^activite/standard/(?P<pk>\d+)/print/confirm/$', activite_standard_print_confirm, name='activite_standard_print_confirm'),
	url(r'^activite/standard/(?P<pk>\d+)/print/pdf/$', activite_standard_print_pdf, name='activite_standard_print_pdf'),

	#-----------------------------------------------------
	#----------- CRUD ALLOCATION PLACE MARCHE ------------
	#-----------------------------------------------------	
	url(r'^activite/allocation_place_marche/$', allocation_place_marche_list, name='allocation_place_marche_list'),
	url(r'^activite/allocation_place_marche/create/$', allocation_place_marche_create, name='allocation_place_marche_create'),
	url(r'^activite/allocation_place_marche/(?P<pk>\d+)/update/$', allocation_place_marche_update, name='allocation_place_marche_update'),
	url(r'^activite/allocation_place_marche/(?P<pk>\d+)/delete/$', allocation_place_marche_delete, name='allocation_place_marche_delete'),	
	url(r'^activite/allocation_place_marche/(?P<pk>\d+)/upload/$', allocation_place_marche_upload, name='allocation_place_marche_upload'),
	url(r'^activite/allocation_place_marche/validate/$', allocation_place_marche_validate, name='allocation_place_marche_validate'),
	url(r'^activite/allocation_place_marche/ecriture/$', allocation_place_marche_ecriture, name='allocation_place_marche_ecriture'),

	#-----------------------------------------------------
	#---------------- CRUD ACTIVITE MARCHE ---------------
	#-----------------------------------------------------	
	url(r'^activite/marche/$', activite_marche_list, name='activite_marche_list'),
	url(r'^activite/marche/create/$', activite_marche_create, name='activite_marche_create'),
	url(r'^activite/marche/(?P<pk>\d+)/update/$', activite_marche_update, name='activite_marche_update'),
	url(r'^activite/marche/(?P<pk>\d+)/delete/$', activite_marche_delete, name='activite_marche_delete'),
	url(r'^activite/marche/validate/$', activite_marche_validate, name='activite_marche_validate'),
	url(r'^activite/marche/ecriture/$', activite_marche_ecriture, name='activite_marche_ecriture'),


	# Print carte activite marché
	url(r'^activite/marche/(?P<pk>\d+)/print/$', activite_marche_print, name='activite_marche_print'),
	url(r'^activite/marche/(?P<pk>\d+)/print/authorization/$', activite_marche_print_authorization, name='activite_marche_print_authorization'),
	url(r'^activite/marche/(?P<pk>\d+)/print/confirm/$', activite_marche_print_confirm, name='activite_marche_print_confirm'),
	url(r'^activite/marche/(?P<pk>\d+)/print/pdf/$', activite_marche_print_pdf, name='activite_marche_print_pdf'),

	#-----------------------------------------------------
	#------------ CRUD ACTIVITE EXCEPTIONNELLE -----------
	#-----------------------------------------------------		
	url(r'^activite/exceptionnelle/$', activite_exceptionnelle_list, name='activite_exceptionnelle_list'),
	url(r'^activite/exceptionnelle/create/$', activite_exceptionnelle_create, name='activite_exceptionnelle_create'),
	url(r'^activite/exceptionnelle/(?P<pk>\d+)/update/$', activite_exceptionnelle_update, name='activite_exceptionnelle_update'),
	url(r'^activite/exceptionnelle/(?P<pk>\d+)/delete/$', activite_exceptionnelle_delete, name='activite_exceptionnelle_delete'),	
	url(r'^activite/exceptionnelle/validate/$', activite_exceptionnelle_validate, name='activite_exceptionnelle_validate'),
	url(r'^activite/exceptionnelle/ecriture/$', activite_exceptionnelle_ecriture, name='activite_exceptionnelle_ecriture'),
	
	#-----------------------------------------------------
	#------------ CRUD VISITE SITE TOURISTIQUE -----------
	#-----------------------------------------------------		
	url(r'^activite/visite_site_touristique/$', visite_site_touristique_list, name='visite_site_touristique_list'),
	url(r'^activite/visite_site_touristique/create/$', visite_site_touristique_create, name='visite_site_touristique_create'),
	url(r'^activite/visite_site_touristique/(?P<pk>\d+)/update/$', visite_site_touristique_update, name='visite_site_touristique_update'),
	url(r'^activite/visite_site_touristique/(?P<pk>\d+)/delete/$', visite_site_touristique_delete, name='visite_site_touristique_delete'),	
	url(r'^activite/visite_site_touristique/validate/$', visite_site_touristique_validate, name='visite_site_touristique_validate'),
	url(r'^activite/visite_site_touristique/ecriture/$', visite_site_touristique_ecriture, name='visite_site_touristique_ecriture'),

	#-----------------------------------------------------
	#--------- CRUD ALLOCATION PANNEAU PUBLICITAIRE ------
	#-----------------------------------------------------	
	url(r'^activite/allocation_panneau_publicitaire/$', allocation_panneau_publicitaire_list, name='allocation_panneau_publicitaire_list'),
	url(r'^activite/allocation_panneau_publicitaire/create/$', allocation_panneau_publicitaire_create, name='allocation_panneau_publicitaire_create'),
	url(r'^activite/allocation_panneau_publicitaire/(?P<pk>\d+)/update/$', allocation_panneau_publicitaire_update, name='allocation_panneau_publicitaire_update'),
	url(r'^activite/allocation_panneau_publicitaire/(?P<pk>\d+)/delete/$', allocation_panneau_publicitaire_delete, name='allocation_panneau_publicitaire_delete'),	
	url(r'^activite/allocation_panneau_publicitaire/(?P<pk>\d+)/upload/$', allocation_panneau_publicitaire_upload, name='allocation_panneau_publicitaire_upload'),
	url(r'^activite/allocation_panneau_publicitaire/validate/$', allocation_panneau_publicitaire_validate, name='allocation_panneau_publicitaire_validate'),
	url(r'^activite/allocation_panneau_publicitaire/ecriture/$', allocation_panneau_publicitaire_ecriture, name='allocation_panneau_publicitaire_ecriture'),

	#-----------------------------------------------------
	#------------- CRUD PUBLICITE MURS-CLOTURES ----------
	#-----------------------------------------------------	
	url(r'^activite/publicite_mur_cloture/$', publicite_mur_cloture_list, name='publicite_mur_cloture_list'),
	url(r'^activite/publicite_mur_cloture/create/$', publicite_mur_cloture_create, name='publicite_mur_cloture_create'),
	url(r'^activite/publicite_mur_cloture/(?P<pk>\d+)/update/$', publicite_mur_cloture_update, name='publicite_mur_cloture_update'),
	url(r'^activite/publicite_mur_cloture/(?P<pk>\d+)/delete/$', publicite_mur_cloture_delete, name='publicite_mur_cloture_delete'),	
	url(r'^activite/publicite_mur_cloture/(?P<pk>\d+)/upload/$', publicite_mur_cloture_upload, name='publicite_mur_cloture_upload'),
	url(r'^activite/publicite_mur_cloture/validate/$', publicite_mur_cloture_validate, name='publicite_mur_cloture_validate'),
	url(r'^activite/publicite_mur_cloture/ecriture/$', publicite_mur_cloture_ecriture, name='publicite_mur_cloture_ecriture'),

	#-----------------------------------------------------
	#----------- CRUD ALLOCATION ESPACE PUBLIQUE ---------
	#-----------------------------------------------------	
	url(r'^foncier/allocation_espace_publique/$', allocation_espace_publique_list, name='allocation_espace_publique_list'),
	url(r'^foncier/allocation_espace_publique/create/$', allocation_espace_publique_create, name='allocation_espace_publique_create'),
	url(r'^foncier/allocation_espace_publique/(?P<pk>\d+)/update/$', allocation_espace_publique_update, name='allocation_espace_publique_update'),
	url(r'^foncier/allocation_espace_publique/(?P<pk>\d+)/delete/$', allocation_espace_publique_delete, name='allocation_espace_publique_delete'),	
	url(r'^foncier/allocation_espace_publique/(?P<pk>\d+)/upload/$', allocation_espace_publique_upload, name='allocation_espace_publique_upload'),
	url(r'^foncier/allocation_espace_publique/validate/$', allocation_espace_publique_validate, name='allocation_espace_publique_validate'),
	url(r'^foncier/allocation_espace_publique/ecriture/$', allocation_espace_publique_ecriture, name='allocation_espace_publique_ecriture'),

	#-----------------------------------------------------
	#------------ CRUD ACTIVITE ARRET SERVICE ------------
	#-----------------------------------------------------	
	url(r'^activite/activite_arret_service/$', activite_arret_service_list, name='activite_arret_service_list'),
	url(r'^activite/activite_arret_service/create/$', activite_arret_service_create, name='activite_arret_service_create'),
	url(r'^activite/activite_arret_service_standard/(?P<pk>\d+)/(?P<ent>\d+)/create/$', activite_arret_service_create, name='activite_arret_service_create'),
	url(r'^activite/activite_arret_service/(?P<pk>\d+)/update/$', activite_arret_service_update, name='activite_arret_service_update'),
	url(r'^activite/activite_arret_service/(?P<pk>\d+)/delete/$', activite_arret_service_delete, name='activite_arret_service_delete'),
	url(r'^activite/activite_arret_service/(?P<pk>\d+)/upload/$', activite_arret_service_upload, name='activite_arret_service_upload'),
	url(r'^activite/activite_arret_service/validate/$', activite_arret_service_validate, name='activite_arret_service_validate'),

	#-----------------------------------------------------
	#--------------------- AUTOCOMPLETE ------------------
	#-----------------------------------------------------
	# Autocomplete Activité (Standard - Marche - Publique)
    url(r'^activite/standard/autocomplete/$', activite_standard_auto_complete, name='activite_standard_auto_complete'),
    url(r'^activite/marche/autocomplete/$', activite_marche_auto_complete, name='activite_marche_auto_complete'),
    url(r'^activite/publique/autocomplete/$', activite_publique_auto_complete, name='activite_publique_auto_complete'),

	url(r'^activite/droit_place_marche/autocomplete/$', droit_place_marche_autocomplete, name='droit_place_marche_autocomplete'),
	url(r'^activite/allocation_place_marche/autocomplete/$', allocation_place_marche_autocomplete, name='allocation_place_marche_autocomplete'),
	url(r'^activite/allocation_parcelle_publique/autocomplete/$', allocation_parcelle_publique_autocomplete, name='allocation_parcelle_publique_autocomplete'),

	#-----------------------------------------------------
	#--------- LOGOUT/LOGIN URL !!! IMPORTANT !!! --------
	#-----------------------------------------------------  
	url(r'^activite/standard/login/$', LoginView.as_view(), {'template_name': 'login.html', 'authentication_form': LoginForm}, name='login'),
	url(r'^activite/allocation_place_marche/login/$', LoginView.as_view(), {'template_name': 'login.html', 'authentication_form': LoginForm}, name='login'),
	url(r'^activite/marche/login/$', LoginView.as_view(), {'template_name': 'login.html', 'authentication_form': LoginForm}, name='login'),
	url(r'^activite/exceptionnelle/login/$', LoginView.as_view(), {'template_name': 'login.html', 'authentication_form': LoginForm}, name='login'),
	url(r'^activite/visite_site_touristique/login/$', LoginView.as_view(), {'template_name': 'login.html', 'authentication_form': LoginForm}, name='login'),
	url(r'^activite/allocation_panneau_publicitaire/login/$', LoginView.as_view(), {'template_name': 'login.html', 'authentication_form': LoginForm}, name='login'),
	url(r'^activite/publicite_mur_cloture/login/$', LoginView.as_view(), {'template_name': 'login.html', 'authentication_form': LoginForm}, name='login'),
	url(r'^foncier/allocation_espace_publique/login/$', LoginView.as_view(), {'template_name': 'login.html', 'authentication_form': LoginForm}, name='login'),
	url(r'^activite/activite/activite_arret_service/login/$', LoginView.as_view(), {'template_name': 'login.html', 'authentication_form': LoginForm}, name='login'),

]