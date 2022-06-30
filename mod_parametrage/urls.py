from django.conf.urls import url
from .views import * 

urlpatterns = [
	
	#-----------------------------------------------------
	#------------------ CRUD NOTIFICATION ----------------
	#-----------------------------------------------------	
	url(r'^parametrage/notification/$', notification_list, name='notification_list'),
	url(r'^parametrage/notification/create/$', notification_create, name='notification_create'),
	url(r'^parametrage/notification/(?P<pk>\d+)/update/$', notification_update, name='notification_update'),
	url(r'^parametrage/notification/(?P<pk>\d+)/open/$', notification_open, name='notification_open'),

    # Charger la liste d'avenue/rue d'un quartier
    url( r'^parametrage/adresse/quertier/load_rueavenue/$', adresse_rue_avenue_by_zone, name='adresse_rue_avenue_by_zone'),

    # Autocomplete d'adresse
    url( r'^parametrage/adresse/zone/autocomplete/$', adresse_zone_autocomplete, name='adresse_zone_autocomplete'),

    # Autocomplete rue et avenue
    url( r'^parametrage/adresse/zone/quartier/(?P<quartier_id>\d+)/rue_avenue/autocomplete/$', adresse_rue_avenue_autocomplete, name='adresse_rue_avenue_autocomplete'),

   	# Chercher l'accessblité d'une rue ou avenue
   	url( r'^parametrage/adresse/rue_avenue/load_accesibilite/$', load_accessibilite_by_rue_avenue, name='load_accessibilite_by_rue_avenue'),

]