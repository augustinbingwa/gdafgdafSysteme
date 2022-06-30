from django.conf.urls import url
from django.contrib.auth.views import LoginView
from gdaf.forms import LoginForm
from mod_documents.subviews.view_non_redevabilite import *
from mod_documents.subviews.view_recapitulatif_de_note import *

urlpatterns = [
    # AFFICHAGE DES DOCUMENTS
    url(r'^att_non_redevabilite/$', non_redevabilite_list, name='non_redevabilite_list'),
    url(r'^att_non_redevabilite/create/$', non_redevabilite_create, name='non_redevabilite_create'),
    url(r'^att_non_redevabilite/(?P<pk>\d+)/print/$', non_redevabilite_pdf, name='non_redevabilite_pdf'),
    url(r'^att_non_redevabilite/(?P<pk>\d+)/update/$', non_redevabilite_update, name='non_redevabilite_update'),
    url(r'^finance/avis_imposition/login/$', LoginView.as_view(),{'template_name': 'login.html', 'authentication_form': LoginForm}, name='login'),
    # recapitulatif de note
    url(r'^recapitulatif_de_note/recapitulatif_de_note_list/$', recapitulatif_de_note_list, name='recapitulatif_de_note_list'),



]