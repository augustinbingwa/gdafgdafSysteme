from django.conf.urls import url 
from .views import *

urlpatterns = [
	# ------------------------------------------------------------------------
	# ------------------------ REPORTS RESUME MODULES ------------------------
	# ------------------------------------------------------------------------
	# Page
	url(r'^gdaf/reporting/module/resume/$', report_module_resume, name='report_module_resume'),

	# Module Foncier PDF
	url(r'^gdaf/reporting/module/resume/print/pdf/$', report_module_resume_print_pdf, name='report_module_resume_print_pdf'),	

	# ------------------------------------------------------------------------
	# ------------------- REPORTS CENTRALISATION JOURNALIERE -----------------
	# ------------------------------------------------------------------------
	# Page
	url(r'^gdaf/reporting/centralisation/journaliere/ni/$', centralisation_journaliere_ni, name='centralisation_journaliere_ni'),	
	url(r'^gdaf/reporting/centralisation/journaliere/recette/$', centralisation_journaliere_recette, name='centralisation_journaliere_recette'),	
	url(r'^gdaf/reporting/centralisation/reconsiliation/banque/$', reconsiliation_banque, name='reconsiliation_banque'),
	url(r'^gdaf/reporting/centralisation/reconsiliation/banque/$', reconsiliation_banque, name='reconsiliation_banque'),
	url(r'^gdaf/reporting/centralisation/reconsiliation/banque/modul/$', reconsiliation_banque_modul, name='reconsiliation_banque_modul'),
	url(r'^gdaf/reporting/centralisation/reconsiliation/banque/imposition/$', reconsiliation_banque_type_imposition, name='reconsiliation_banque_type_imposition'),
	url(r'^gdaf/reporting/centralisation/reconsiliation/banque/paiement/$', reconsiliation_banque_paiement, name='reconsiliation_banque_paiement'),
	url(r'^gdaf/reporting/centralisation/reconsiliation/banque/all/$', reconsiliation_banque_all, name='reconsiliation_banque_all'),

	# Print
	url(r'^gdaf/reporting/centralisation/journaliere/ni/print/pdf/$', centralisation_journaliere_ni_print_pdf, name='centralisation_journaliere_ni_print_pdf'),
	url(r'^gdaf/reporting/centralisation/journaliere/recette/print/pdf/$', centralisation_journaliere_recette_print_pdf, name='centralisation_journaliere_recette_print_pdf'),	
	
	# ------------------------------------------------------------------------
	# ------------------- REPORTS RECAPITULATIF JOURNALIERE ------------------
	# ------------------------------------------------------------------------
	# Page
	url(r'^gdaf/reporting/recapitulatif/journalier/declarant/$', recapitulatif_journalier_declarant, name='recapitulatif_journalier_declarant'),
	url(r'^gdaf/reporting/recapitulatif/journalier/montant/$', recapitulatif_journalier_montant, name='recapitulatif_journalier_montant'),
	url(r'^gdaf/reporting/recapitulatif/journalier/recette/$', recapitulatif_journalier_recette, name='recapitulatif_journalier_recette'),
	
	# Print
	url(r'^gdaf/reporting/recapitulatif/journalier/declarant/print/pdf/$', recapitulatif_journalier_declarant_print_pdf, name='recapitulatif_journalier_declarant_print_pdf'),
	url(r'^gdaf/reporting/recapitulatif/journalier/montant/print/pdf/$', recapitulatif_journalier_montant_print_pdf, name='recapitulatif_journalier_montant_print_pdf'),
	url(r'^gdaf/reporting/recapitulatif/journalier/recette/print/pdf/$', recapitulatif_journalier_recette_print_pdf, name='recapitulatif_journalier_recette_print_pdf'),
		
]