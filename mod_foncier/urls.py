from django.conf.urls import url

from django.contrib.auth.views import LoginView
from gdaf.forms import LoginForm
 
from .views import *

urlpatterns = [
	# ----------------------------------------------------------------------------------------------------------------------------------
	url(r'^foncier/foncier_parcelle/$', foncier_parcelle_list, name='foncier_parcelle_list'),
	url(r'^foncier/foncier_parcelle/create/$', foncier_parcelle_create, name='foncier_parcelle_create'),
	url(r'^foncier/foncier_parcelle/(?P<pk>\d+)/update/$', foncier_parcelle_update, name='foncier_parcelle_update'),
	url(r'^foncier/foncier_parcelle/(?P<pk>\d+)/delete/$', foncier_parcelle_delete, name='foncier_parcelle_delete'),
	url(r'^foncier/foncier_parcelle/(?P<pk>\d+)/upload/$', foncier_parcelle_upload, name='foncier_parcelle_upload'),
	url(r'^foncier/foncier_parcelle/(?P<pk>\d+)/upload_temp/$', foncier_parcelle_upload_temp, name='foncier_parcelle_upload_temp'),
	 url(r'^foncier/foncier_parcelle/(?P<pk>\d+)/transferts/$', parcelle_transfert, name='parcelle_transfert'),
	url(r'^foncier/foncier_parcelle/(?P<pk>\d+)/changevalidation/$', foncier_parcelle_change_validation, name='foncier_parcelle_change_validation'),
	url(r'^foncier/foncier_parcelle/validate/$', foncier_parcelle_validate, name='foncier_parcelle_validate'),
    url(r'^foncier/transfert_parc/autocomplete/$', parcelle_transfert_autocomplete, name='parcelle_transfert_autocomplete'),
	
	# ------------------------------export to pdf---------------------------------------------------------------------------------------
    url(r'^foncier/foncier_attestation/pdf/(?P<pk>\d+)/$', attestation_parcelle_pdf, name='attestation_parcelle_pdf'),
	
	# ----------------------------------------------------------------------------------------------------------------------------------
	url(r'^foncier/foncier_parcelle/(?P<pk>\d+)/create_expertise/$', foncier_parcelle_create_expertise, name='foncier_parcelle_create_expertise'),
	
	# ----------------------------------------------------------------------------------------------------------------------------------
	url(r'^foncier/foncier_expertise/$', foncier_expertise_list, name='foncier_expertise_list'),
	url(r'^foncier/foncier_expertise/create/$', foncier_expertise_create, name='foncier_expertise_create'),
	url(r'^foncier/foncier_expertise/(?P<pk>\d+)/update/$', foncier_expertise_update, name='foncier_expertise_update'),
	url(r'^foncier/foncier_expertise/(?P<pk>\d+)/upload/$', foncier_expertise_upload, name='foncier_expertise_upload'),
	url(r'^foncier/foncier_expertise/validate/$', foncier_expertise_validate, name='foncier_expertise_validate'),
	url(r'^foncier/foncier_expertise/ecriture/$', foncier_expertise_ecriture, name='foncier_expertise_ecriture'),

	# Annuler une déclaration (partielle ou totale)
	url(r'^foncier/foncier_expertise/(?P<pk>\d+)/delete/$', foncier_expertise_delete, name='foncier_expertise_delete'),
	url(r'^foncier/foncier_expertise/delete_action/$', foncier_expertise_delete_action, name='foncier_expertise_delete_action'),
	
	# Impresion l'aperçu de la note
	url(r'^foncier/foncier_expertise/note/apercu/(?P<pk>\d+)/print/$', apercu_ni_print_pdf, name='apercu_ni_print_pdf'),

	# ----------------------------------------------------------------------------------------------------------------------------------	
	url(r'^foncier/foncier_expertise/(?P<pk>\d+)/caracteristique/$', foncier_expertise_caracteristique, name='foncier_expertise_caracteristique'),
	url(r'^foncier/foncier_expertise/caracteristique_add/$', foncier_expertise_caracteristique_create, name='foncier_expertise_caracteristique_create'),
	url(r'^foncier/foncier_expertise/caracteristique_delete/$', foncier_expertise_caracteristique_delete, name='foncier_expertise_caracteristique_delete'),
	
	# ----------------------------------------------------------------------------------------------------------------------------------
	url(r'^foncier/parcelle_publique/$', foncier_parcelle_publique_list, name='foncier_parcelle_publique_list'),
	url(r'^foncier/parcelle_publique/create/$', foncier_parcelle_publique_create, name='foncier_parcelle_publique_create'),
	url(r'^foncier/parcelle_publique/(?P<pk>\d+)/update/$', foncier_parcelle_publique_update, name='foncier_parcelle_publique_update'),
	url(r'^foncier/parcelle_publique/(?P<pk>\d+)/delete/$', foncier_parcelle_publique_delete, name='foncier_parcelle_publique_delete'),
	url(r'^foncier/parcelle_publique/validate/$', foncier_parcelle_publique_validate, name='foncier_parcelle_publique_validate'),

	# ----------------------------------------------------------------------------------------------------------------------------------
	url(r'^foncier/foncier_expertise/autocomplete/$', parcelle_autocomplete, name='parcelle_autocomplete'),
	url(r'^foncier/parcelle_publique/autocomplete/$', foncier_non_occupe_valide_autocomplete, name='foncier_non_occupe_valide_autocomplete'),

	# Charger les impots
	url(r'^foncier/parcelle/load_impot/$', load_impot_by_accessibilite, name='load_impot_by_accessibilite'),

	#-----------------------------------------------------
	#--------- LOGOUT/LOGIN URL !!! IMPORTANT !!! --------
	#-----------------------------------------------------  
	url(r'^foncier/foncier_parcelle/login/$', LoginView.as_view(), {'template_name': 'login.html', 'authentication_form': LoginForm}, name='login'),
	url(r'^foncier/foncier_expertise/login/$', LoginView.as_view(), {'template_name': 'login.html', 'authentication_form': LoginForm}, name='login'),
	url(r'^foncier/parcelle_publique/login/$', LoginView.as_view(), {'template_name': 'login.html', 'authentication_form': LoginForm}, name='login'),
]