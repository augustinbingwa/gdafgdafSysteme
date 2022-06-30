from django.conf.urls import url
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from django.contrib.auth.views import login
from gdaf.forms import LoginForm

from mod_crm.views import * #Import de tous les views

urlpatterns = [
    # Contribuable Personne Physique
    url(r'^crm/contribuable/physique/$', physique_list, name='physique_list'),
    url(r'^crm/contribuable/physique/create/$', physique_create, name='physique_create'),
    url(r'^crm/contribuable/physique/(?P<pk>\d+)/update/$', physique_update, name='physique_update'),
    url(r'^crm/contribuable/physique/(?P<pk>\d+)/delete/$', physique_delete, name='physique_delete'),
    url(r'^crm/contribuable/physique/(?P<pk>\d+)/upload/$', physique_upload, name='physique_upload'),
    url(r'^crm/contribuable/physique/(?P<pk>\d+)/upload_temp/$', physique_upload_temp, name='physique_upload_temp'),
    url(r'^crm/contribuable/physique/(?P<pk>\d+)/changevalidation/$', physique_change_validation, name='physique_change_validation'),
    url(r'^crm/contribuable/physique/validate/$', physique_validate, name='physique_validate'),
    
    # Contribuable Personne Morale
    url(r'^crm/contribuable/morale/$', morale_list, name='morale_list'),
    url(r'^crm/contribuable/morale/create/$', morale_create, name='morale_create'),
    url(r'^crm/contribuable/morale/(?P<pk>\d+)/update/$', morale_update, name='morale_update'),
    url(r'^crm/contribuable/morale/(?P<pk>\d+)/delete/$', morale_delete, name='morale_delete'),
    url(r'^crm/contribuable/morale/(?P<pk>\d+)/upload/$', morale_upload, name='morale_upload'),
    url(r'^crm/contribuable/morale/validate/$', morale_validate, name='morale_validate'),

    # Autocomplete
    url( r'^crm/contribuable/autocomplete/$', contribuable_auto_complete, name='contribuable_auto_complete'),

    # Export des données vers (pdf, excel, word, csv)
    url(r'^crm/contribuable/physique/export/$', physique_export, name='physique_export'),

    #-----------------------------------------------------
    #--------- LOGOUT/LOGIN URL !!! IMPORTANT !!! --------
    #-----------------------------------------------------  
    url(r'^crm/contribuable/physique/login/$', login, {'template_name': 'login.html', 'authentication_form': LoginForm}, name='login'),
    url(r'^crm/contribuable/morale/login/$', login, {'template_name': 'login.html', 'authentication_form': LoginForm}, name='login'),
]