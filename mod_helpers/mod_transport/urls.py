from django.urls import path
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from django.contrib.auth.views import LoginView
from gdaf.forms import LoginForm

from .import views

urlpatterns = [

	#-----------------------------------------------------
	#------------------- CRUD VEHICULE -------------------
	#-----------------------------------------------------	
	path('transport/vehicule/', views.vehicule_list, name='vehicule_list'),
	path('transport/vehicule/create/', views.vehicule_create, name='vehicule_create'),
	path('transport/vehicule/<int:pk>/update/', views.vehicule_update, name='vehicule_update'),
	path('transport/vehicule/<int:pk>/delete/', views.vehicule_delete, name='vehicule_delete'),
	path('transport/vehicule/validate/', views.vehicule_validate, name='vehicule_validate'),

	#Carte rose : Upload file
	path('transport/vehicule/carterose/<int:pk>/upload/', views.vehicule_upload, name='vehicule_upload'),
	path('transport/vehicule/carterose/<int:pk>/upload_temp/', views.vehicule_upload_temp, name='vehicule_upload_temp'),

	#-----------------------------------------------------
	#------------- CRUD VEHICULE PROPRIETAIRE ------------
	#-----------------------------------------------------	
	path('transport/vehicule_proprietaire/', views.vehicule_proprietaire_list, name='vehicule_proprietaire_list'),
	path('transport/vehicule_proprietaire/<int:pk>/update/', views.vehicule_proprietaire_update, name='vehicule_proprietaire_update'),
	path('transport/vehicule_proprietaire/ecriture/', views.vehicule_proprietaire_ecriture, name='vehicule_proprietaire_ecriture'),

	#Print carte proprietaire
	path('transport/vehicule_proprietaire/<int:pk>/print/', views.vehicule_proprietaire_print, name='vehicule_proprietaire_print'),
	path('transport/vehicule_proprietaire/<int:pk>/print/authorization/', views.vehicule_proprietaire_print_authorization, name='vehicule_proprietaire_print_authorization'),
	path('transport/vehicule_proprietaire/<int:pk>/print/confirm/', views.vehicule_proprietaire_print_confirm, name='vehicule_proprietaire_print_confirm'),
	path('transport/vehicule_proprietaire/<int:pk>/print/pdf/', views.vehicule_proprietaire_print_pdf, name='vehicule_proprietaire_print_pdf'),

	#-----------------------------------------------------
	#--------------- CRUD VEHICULE ACTIVITE --------------
	#-----------------------------------------------------	
	path('transport/vehicule_activite/', views.vehicule_activite_list, name='vehicule_activite_list'),
	path('transport/vehicule_activite/create/', views.vehicule_activite_create, name='vehicule_activite_create'),
	path('transport/vehicule_activite/<int:pk>/update/', views.vehicule_activite_update, name='vehicule_activite_update'),
	path('transport/vehicule_activite/<int:pk>/delete/', views.vehicule_activite_delete, name='vehicule_activite_delete'),
	path('transport/vehicule_activite/validate/', views.vehicule_activite_validate, name='vehicule_activite_validate'),
	path('transport/vehicule_activite/ecriture/', views.vehicule_activite_ecriture, name='vehicule_activite_ecriture'),

	# Génération de l'écriture de la note des activités externe/temporaire
	path('transport/vehicule_activite/ecriture_externe/', views.vehicule_activite_ecriture_externe, name='vehicule_activite_ecriture_externe'),

	

	#Carte rose : Upload file
	path('transport/vehicule_activite/carterose/<int:pk>/upload/', views.vehicule_activite_upload, name='vehicule_activite_upload'),

	#Print carte activite
	path('transport/vehicule_activite/<int:pk>/print/', views.vehicule_activite_print, name='vehicule_activite_print'),
	path('transport/vehicule_activite/<int:pk>/print/authorization/', views.vehicule_activite_print_authorization, name='vehicule_activite_print_authorization'),
	path('transport/vehicule_activite/<int:pk>/print/confirm/', views.vehicule_activite_print_confirm, name='vehicule_activite_print_confirm'),
	path('transport/vehicule_activite/<int:pk>/print/pdf/', views.vehicule_activite_print_pdf, name='vehicule_activite_print_pdf'),

	#-----------------------------------------------------
	#---------- CRUD VEHICULE ACTIVITE DUPLICATA ---------
	#-----------------------------------------------------	
	path('transport/vehicule_activite/duplicata/', views.vehicule_activite_duplicata_list, name='vehicule_activite_duplicata_list'),
	path('transport/vehicule_activite/duplicata/create/', views.vehicule_activite_duplicata_create, name='vehicule_activite_duplicata_create'),
	path('transport/vehicule_activite/duplicata/<int:pk>/update/', views.vehicule_activite_duplicata_update, name='vehicule_activite_duplicata_update'),
	path('transport/vehicule_activite/duplicata/<int:pk>/delete/', views.vehicule_activite_duplicata_delete, name='vehicule_activite_duplicata_delete'),
	path('transport/vehicule_activite/duplicata/validate/', views.vehicule_activite_duplicata_validate, name='vehicule_activite_duplicata_validate'),
	path('transport/vehicule_activite/<int:pk>/arret/', views.vehicule_activite_arretEtReouverture, name='vehicule_activite_arretEtReouverture'),

	#Print duplicata carte professionnelle
	path('transport/vehicule_activite/duplicata/<int:pk>/print/', views.vehicule_activite_duplicata_print, name='vehicule_activite_duplicata_print'),
	path('transport/vehicule_activite/duplicata/<int:pk>/print/authorization/', views.vehicule_activite_duplicata_print_authorization, name='vehicule_activite_duplicata_print_authorization'),
	path('transport/vehicule_activite/duplicata/<int:pk>/print/confirm/', views.vehicule_activite_duplicata_print_confirm, name='vehicule_activite_duplicata_print_confirm'),
	path('transport/vehicule_activite/duplicata/<int:pk>/print/pdf/', views.vehicule_activite_duplicata_print_pdf, name='vehicule_activite_duplicata_print_pdf'),

	#-----------------------------------------------------
	#-------- CRUD VEHICULE PROPRIETAIRE DUPLICATA -------
	#-----------------------------------------------------	
	path('transport/vehicule_proprietaire/duplicata/', views.vehicule_proprietaire_duplicata_list, name='vehicule_proprietaire_duplicata_list'),
	path('transport/vehicule_proprietaire/duplicata/create/', views.vehicule_proprietaire_duplicata_create, name='vehicule_proprietaire_duplicata_create'),
	path('transport/vehicule_proprietaire/duplicata/<int:pk>/update/', views.vehicule_proprietaire_duplicata_update, name='vehicule_proprietaire_duplicata_update'),
	path('transport/vehicule_proprietaire/duplicata/<int:pk>/delete/', views.vehicule_proprietaire_duplicata_delete, name='vehicule_proprietaire_duplicata_delete'),
	path('transport/vehicule_proprietaire/duplicata/validate/', views.vehicule_proprietaire_duplicata_validate, name='vehicule_proprietaire_duplicata_validate'),

	#Print duplicata carte proprietaire
	path('transport/vehicule_proprietaire/duplicata/<int:pk>/print/', views.vehicule_proprietaire_duplicata_print, name='vehicule_proprietaire_duplicata_print'),
	path('transport/vehicule_proprietaire/duplicata/<int:pk>/print/authorization/', views.vehicule_proprietaire_duplicata_print_authorization, name='vehicule_proprietaire_duplicata_print_authorization'),
	path('transport/vehicule_proprietaire/duplicata/<int:pk>/print/confirm/', views.vehicule_proprietaire_duplicata_print_confirm, name='vehicule_proprietaire_duplicata_print_confirm'),
	path('transport/vehicule_proprietaire/duplicata/<int:pk>/print/pdf/', views.vehicule_proprietaire_duplicata_print_pdf, name='vehicule_proprietaire_duplicata_print_pdf'),

	#-----------------------------------------------------
	#------------ CRUD VEHICULE STATIONNEMENT ------------
	#-----------------------------------------------------	
	path('transport/vehicule_stationnement/', views.vehicule_stationnement_list, name='vehicule_stationnement_list'),

	#-----------------------------------------------------
	#------------------- AUTOCOMPLETE --------------------
	#-----------------------------------------------------	
	path('transport/vehicule/autocomplete/', views.vehicule_autocomplete, name='vehicule_autocomplete'),
	path('transport/vehicule_valide/autocomplete/', views.vehicule_valide_autocomplete, name='vehicule_valide_autocomplete'),

	path('transport/vehicule_has_plaque/autocomplete/', views.vehicule_has_plaque_autocomplete, name='vehicule_has_plaque_autocomplete'),
	path('transport/vehicule_has_plaque_valide/autocomplete/', views.vehicule_has_plaque_valide_autocomplete, name='vehicule_has_plaque_valide_autocomplete'),
	path('transport/vehicule_no_plaque_valide/autocomplete/', views.vehicule_no_plaque_valide_autocomplete, name='vehicule_no_plaque_valide_autocomplete'),
	
	path('transport/vehicule_activite/autocomplete/', views.vehicule_activite_autocomplete, name='vehicule_activite_autocomplete'),
	path('transport/vehicule/modele/autocomplete/', views.vehicule_modele_autocomplete, name='vehicule_modele_autocomplete'),
	path('transport/vehicule_proprietaire/autocomplete/', views.vehicule_proprietaire_autocomplete, name='vehicule_proprietaire_autocomplete'),
	
	#-----------------------------------------------------
	#---------------------- HELPERS ----------------------
	#-----------------------------------------------------
	# Cherher le sous catégorie d'un véhicule (Utilisé dans Vehicule Form)
	path('transport/vehicule/sous_categorie/', views.vehicule_get_sous_categorie, name='vehicule_get_sous_categorie'),
	
	#-----------------------------------------------------
	#--------- LOGOUT/LOGIN URL !!! IMPORTANT !!! --------
	#-----------------------------------------------------  
	path('transport/vehicule/login/', LoginView.as_view(), {'template_name': 'login.html', 'authentication_form': LoginForm}, name='login'),
	path('transport/vehicule_proprietaire/login/', LoginView.as_view(), {'template_name': 'login.html', 'authentication_form': LoginForm}, name='login'),
	path('transport/vehicule_activite/login/', LoginView.as_view(), {'template_name': 'login.html', 'authentication_form': LoginForm}, name='login'),
	path('transport/vehicule_activite/duplicata/login/', LoginView.as_view(), {'template_name': 'login.html', 'authentication_form': LoginForm}, name='login'),
	path('transport/vehicule_proprietaire/duplicata/login/', LoginView.as_view(), {'template_name': 'login.html', 'authentication_form': LoginForm}, name='login'),
]