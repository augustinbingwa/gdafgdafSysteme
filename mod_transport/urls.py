from django.conf.urls import url
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from django.contrib.auth.views import LoginView
from gdaf.forms import LoginForm

from .import views

urlpatterns = [

	#-----------------------------------------------------
	#------------------- CRUD VEHICULE -------------------
	#-----------------------------------------------------	
	url(r'^transport/vehicule/$', views.vehicule_list, name='vehicule_list'),
	url(r'^transport/vehicule/create/$', views.vehicule_create, name='vehicule_create'),
	url(r'^transport/vehicule/(?P<pk>\d+)/update/$', views.vehicule_update, name='vehicule_update'),
	url(r'^transport/vehicule/(?P<pk>\d+)/delete/$', views.vehicule_delete, name='vehicule_delete'),
	url(r'^transport/vehicule/validate/$', views.vehicule_validate, name='vehicule_validate'),

	#Carte rose : Upload file
	url(r'^transport/vehicule/carterose/(?P<pk>\d+)/upload/$', views.vehicule_upload, name='vehicule_upload'),
	url(r'^transport/vehicule/carterose/(?P<pk>\d+)/upload_temp/$', views.vehicule_upload_temp, name='vehicule_upload_temp'),	

	#-----------------------------------------------------
	#------------- CRUD VEHICULE PROPRIETAIRE ------------
	#-----------------------------------------------------	
	url(r'^transport/vehicule_proprietaire/$', views.vehicule_proprietaire_list, name='vehicule_proprietaire_list'),
	url(r'^transport/vehicule_proprietaire/(?P<pk>\d+)/update/$', views.vehicule_proprietaire_update, name='vehicule_proprietaire_update'),
	url(r'^transport/vehicule_proprietaire/ecriture/$', views.vehicule_proprietaire_ecriture, name='vehicule_proprietaire_ecriture'),

	#Print carte proprietaire
	url(r'^transport/vehicule_proprietaire/(?P<pk>\d+)/print/$', views.vehicule_proprietaire_print, name='vehicule_proprietaire_print'),
	url(r'^transport/vehicule_proprietaire/(?P<pk>\d+)/print/authorization/$', views.vehicule_proprietaire_print_authorization, name='vehicule_proprietaire_print_authorization'),
	url(r'^transport/vehicule_proprietaire/(?P<pk>\d+)/print/confirm/$', views.vehicule_proprietaire_print_confirm, name='vehicule_proprietaire_print_confirm'),
	url(r'^transport/vehicule_proprietaire/(?P<pk>\d+)/print/pdf/$', views.vehicule_proprietaire_print_pdf, name='vehicule_proprietaire_print_pdf'),

	#-----------------------------------------------------
	#--------------- CRUD VEHICULE ACTIVITE --------------
	#-----------------------------------------------------	
	url(r'^transport/vehicule_activite/$', views.vehicule_activite_list, name='vehicule_activite_list'),
	url(r'^transport/vehicule_activite/create/$', views.vehicule_activite_create, name='vehicule_activite_create'),
	url(r'^transport/vehicule_activite/(?P<pk>\d+)/update/$', views.vehicule_activite_update, name='vehicule_activite_update'),
	url(r'^transport/vehicule_activite/(?P<pk>\d+)/create/$', views.vehicule_activite_arret, name='vehicule_activite_arret'),
	url(r'^transport/vehicule_activite/(?P<pk>\d+)/delete/$', views.vehicule_activite_delete, name='vehicule_activite_delete'),
	url(r'^transport/vehicule_activite/validate/$', views.vehicule_activite_validate, name='vehicule_activite_validate'),
	url(r'^transport/vehicule_activite/ecriture/$', views.vehicule_activite_ecriture, name='vehicule_activite_ecriture'),

	# Génération de l'écriture de la note des activités externe/temporaire
	url(r'^transport/vehicule_activite/ecriture_externe/$', views.vehicule_activite_ecriture_externe, name='vehicule_activite_ecriture_externe'),

	

	#Carte rose : Upload file
	url(r'^transport/vehicule_activite/carterose/(?P<pk>\d+)/upload/$', views.vehicule_activite_upload, name='vehicule_activite_upload'),	

	#Print carte activite
	url(r'^transport/vehicule_activite/(?P<pk>\d+)/print/$', views.vehicule_activite_print, name='vehicule_activite_print'),
	url(r'^transport/vehicule_activite/(?P<pk>\d+)/print/authorization/$', views.vehicule_activite_print_authorization, name='vehicule_activite_print_authorization'),
	url(r'^transport/vehicule_activite/(?P<pk>\d+)/print/confirm/$', views.vehicule_activite_print_confirm, name='vehicule_activite_print_confirm'),
	url(r'^transport/vehicule_activite/(?P<pk>\d+)/print/pdf/$', views.vehicule_activite_print_pdf, name='vehicule_activite_print_pdf'),

	#-----------------------------------------------------
	#---------- CRUD VEHICULE ACTIVITE DUPLICATA ---------
	#-----------------------------------------------------	
	url(r'^transport/vehicule_activite/duplicata/$', views.vehicule_activite_duplicata_list, name='vehicule_activite_duplicata_list'),
	url(r'^transport/vehicule_activite/duplicata/create/$', views.vehicule_activite_duplicata_create, name='vehicule_activite_duplicata_create'),
	url(r'^transport/vehicule_activite/duplicata/(?P<pk>\d+)/update/$', views.vehicule_activite_duplicata_update, name='vehicule_activite_duplicata_update'),
	url(r'^transport/vehicule_activite/duplicata/(?P<pk>\d+)/delete/$', views.vehicule_activite_duplicata_delete, name='vehicule_activite_duplicata_delete'),
	url(r'^transport/vehicule_activite/duplicata/validate/$', views.vehicule_activite_duplicata_validate, name='vehicule_activite_duplicata_validate'),

	#Print duplicata carte professionnelle
	url(r'^transport/vehicule_activite/duplicata/(?P<pk>\d+)/print/$', views.vehicule_activite_duplicata_print, name='vehicule_activite_duplicata_print'),
	url(r'^transport/vehicule_activite/duplicata/(?P<pk>\d+)/print/authorization/$', views.vehicule_activite_duplicata_print_authorization, name='vehicule_activite_duplicata_print_authorization'),
	url(r'^transport/vehicule_activite/duplicata/(?P<pk>\d+)/print/confirm/$', views.vehicule_activite_duplicata_print_confirm, name='vehicule_activite_duplicata_print_confirm'),
	url(r'^transport/vehicule_activite/duplicata/(?P<pk>\d+)/print/pdf/$', views.vehicule_activite_duplicata_print_pdf, name='vehicule_activite_duplicata_print_pdf'),

	#-----------------------------------------------------
	#-------- CRUD VEHICULE PROPRIETAIRE DUPLICATA -------
	#-----------------------------------------------------	
	url(r'^transport/vehicule_proprietaire/duplicata/$', views.vehicule_proprietaire_duplicata_list, name='vehicule_proprietaire_duplicata_list'),
	url(r'^transport/vehicule_proprietaire/duplicata/create/$', views.vehicule_proprietaire_duplicata_create, name='vehicule_proprietaire_duplicata_create'),
	url(r'^transport/vehicule_proprietaire/duplicata/(?P<pk>\d+)/update/$', views.vehicule_proprietaire_duplicata_update, name='vehicule_proprietaire_duplicata_update'), 
	url(r'^transport/vehicule_proprietaire/duplicata/(?P<pk>\d+)/delete/$', views.vehicule_proprietaire_duplicata_delete, name='vehicule_proprietaire_duplicata_delete'),
	url(r'^transport/vehicule_proprietaire/duplicata/validate/$', views.vehicule_proprietaire_duplicata_validate, name='vehicule_proprietaire_duplicata_validate'),

	#Print duplicata carte proprietaire
	url(r'^transport/vehicule_proprietaire/duplicata/(?P<pk>\d+)/print/$', views.vehicule_proprietaire_duplicata_print, name='vehicule_proprietaire_duplicata_print'),
	url(r'^transport/vehicule_proprietaire/duplicata/(?P<pk>\d+)/print/authorization/$', views.vehicule_proprietaire_duplicata_print_authorization, name='vehicule_proprietaire_duplicata_print_authorization'),
	url(r'^transport/vehicule_proprietaire/duplicata/(?P<pk>\d+)/print/confirm/$', views.vehicule_proprietaire_duplicata_print_confirm, name='vehicule_proprietaire_duplicata_print_confirm'),
	url(r'^transport/vehicule_proprietaire/duplicata/(?P<pk>\d+)/print/pdf/$', views.vehicule_proprietaire_duplicata_print_pdf, name='vehicule_proprietaire_duplicata_print_pdf'),

	#-----------------------------------------------------
	#------------ CRUD VEHICULE STATIONNEMENT ------------
	#-----------------------------------------------------	
	url(r'^transport/vehicule_stationnement/$', views.vehicule_stationnement_list, name='vehicule_stationnement_list'),

	#-----------------------------------------------------
	#------------------- AUTOCOMPLETE --------------------
	#-----------------------------------------------------	
	url( r'^transport/vehicule/autocomplete/$', views.vehicule_autocomplete, name='vehicule_autocomplete'),
	url( r'^transport/vehicule_valide/autocomplete/$', views.vehicule_valide_autocomplete, name='vehicule_valide_autocomplete'),

	url( r'^transport/vehicule_has_plaque/autocomplete/$', views.vehicule_has_plaque_autocomplete, name='vehicule_has_plaque_autocomplete'),
	url( r'^transport/vehicule_has_plaque_valide/autocomplete/$', views.vehicule_has_plaque_valide_autocomplete, name='vehicule_has_plaque_valide_autocomplete'),
	url( r'^transport/vehicule_no_plaque_valide/autocomplete/$', views.vehicule_no_plaque_valide_autocomplete, name='vehicule_no_plaque_valide_autocomplete'),
	url( r'^transport/vehicule_activite/autocomplete/$', views.vehicule_activite_autocomplete, name='vehicule_activite_autocomplete'),
	url( r'^transport/vehicule/modele/autocomplete/$', views.vehicule_modele_autocomplete, name='vehicule_modele_autocomplete'),
	url( r'^transport/vehicule_proprietaire/autocomplete/$', views.vehicule_proprietaire_autocomplete, name='vehicule_proprietaire_autocomplete'),


	#-----------------------------------------------------
	#------------ CRUD VEHICULE ARRET SERVICE ------------
	#-----------------------------------------------------	
	url(r'^transport/vehicule_arret_service/$', views.vehicule_arret_service_list, name='vehicule_arret_service_list'),
	url(r'^transport/vehicule_arret_service/create/$', views.vehicule_arret_service_create, name='vehicule_arret_service_create'),
	url(r'^transport/vehicule_arret_service/(?P<pk>\d+)/update/$', views.vehicule_arret_service_update, name='vehicule_arret_service_update'),
	url(r'^transport/vehicule_arret_service/(?P<pk>\d+)/reouverture/$', views.vehicule_reouverture_service, name='vehicule_reouverture_service'),
	url(r'^transport/vehicule_arret_service/(?P<pk>\d+)/delete/$', views.vehicule_arret_service_delete, name='vehicule_arret_service_delete'),
	url(r'^transport/vehicule_arret_service/(?P<pk>\d+)/upload/$', views.vehicule_arret_service_upload, name='vehicule_arret_service_upload'),
	url(r'^transport/vehicule_arret_service/(?P<pk>\d+)/upload_carte/$', views.vehicule_carte_municipale_upload, name='vehicule_carte_municipale_upload'),
	url(r'^transport/vehicule_arret_service/validate/$', views.vehicule_arret_service_validate, name='vehicule_arret_service_validate'),

	#-----------------------------------------------------
	#------------ CRUD VEHICULE TRANSFERT ----------------
	#-----------------------------------------------------
	url(r'^transport/vehicule_transfert/$', views.vehicule_transfert_list, name='vehicule_transfert_list'),
	url(r'^transport/vehicule_transfert/(?P<pk>\d+)/create/$', views.vehicule_transfert_create, name='vehicule_transfert_create'),
	url(r'^transport/vehicule_transfert/(?P<pk>\d+)/update/$', views.vehicule_transfert_update, name='vehicule_transfert_update'),
	url(r'^transport/vehicule_transfert/(?P<pk>\d+)/upload_cr/$', views.vehicule_transfert_upload_cr, name='vehicule_transfert_upload_cr'),
	url(r'^transport/vehicule_transfert/(?P<pk>\d+)/upload_temp/$', views.vehicule_transfert_upload_temp, name='vehicule_transfert_upload_temp'),
	url(r'^transport/vehicule_transfert/(?P<pk>\d+)/delete/$', views.vehicule_transfert_delete, name='vehicule_transfert_delete'),
	url(r'^transport/vehicule_transfert/(?P<pk>\d+)/upload/$', views.vehicule_transfert_upload, name='vehicule_transfert_upload'),
	url(r'^transport/vehicule_transfert/validate/$', views.vehicule_transfert_validate, name='vehicule_transfert_validate'),
	
	#-----------------------------------------------------
	#---------------------- HELPERS ----------------------
	#-----------------------------------------------------
	# Cherher le sous catégorie d'un véhicule (Utilisé dans Vehicule Form)
	url( r'^transport/vehicule/sous_categorie/$', views.vehicule_get_sous_categorie, name='vehicule_get_sous_categorie'),
	
	#-----------------------------------------------------
	#--------- LOGOUT/LOGIN URL !!! IMPORTANT !!! --------
	#-----------------------------------------------------  
	url(r'^transport/vehicule/login/$', LoginView.as_view(template_name='login.html', authentication_form=LoginForm), name='login'),
	url(r'^transport/vehicule_proprietaire/login/$', LoginView.as_view(template_name='login.html', authentication_form=LoginForm), name='login'),
	url(r'^transport/vehicule_activite/login/$', LoginView.as_view(template_name='login.html', authentication_form=LoginForm), name='login'),
	url(r'^transport/vehicule_activite/duplicata/login/$', LoginView.as_view(template_name='login.html',authentication_form=LoginForm), name='login'),
	url(r'^transport/vehicule_proprietaire/duplicata/login/$', LoginView.as_view(template_name='login.html',authentication_form=LoginForm), name='login'),
]