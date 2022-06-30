from django.conf.urls import url

from mod_helpers.views import *

urlpatterns = [
	# Editer la note d'un objet (entité)
	url(r'^helpers/note/(?P<pk>\d+)/(?P<class_name>[-a-zA-Z._]+)/(?P<view_name>[-a-zA-Z._]+)/editer/$', edit_note, name='edit_note'),

	# Annuler la validation d'un objet (entité)
	url(r'^helpers/note/unvalidate/$', unvalidate_entity, name='unvalidate_entity'),

	url(r'^helpers/profile/show/$', show_user_profile, name='show_user_profile'),
]