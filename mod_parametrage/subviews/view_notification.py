from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt

from mod_helpers.hlp_paginator import PaginatorHelpers
from mod_helpers.hlp_error import ErrorsHelpers
from mod_helpers.hlp_operations import OperationsHelpers
from mod_helpers.hlp_notification import NotificationHelpers

from mod_parametrage.models import Notification
from mod_parametrage.forms import NotificationForm
from mod_parametrage.templates import NotificationTemplate

#----------------------------------------------------------------
#----------------- CRUD Gestion des notification ----------------
#----------------------------------------------------------------

@login_required(login_url="login/")
def notification_list(request):
	"""
	Liste des notification par user
	"""
	lst = PaginatorHelpers.get_list_paginator(request, Notification)   
	
	# Lire les notifications
	lst_notification = NotificationHelpers.get_list(request)

	context = {
		'lst': lst,
		'lst_notification':lst_notification,
	}

	return render(request, NotificationTemplate.index, context)

#----------------------------------------------------------------
@login_required(login_url="login/")
def notification_create(request):
	"""
	Création/Ajout d'une notification
	"""
	if request.method == 'POST':
		form = NotificationForm(request.POST)
	else:
		form = NotificationForm()

	return save_notification_form(request, form, NotificationTemplate.create, 'create')

#----------------------------------------------------------------
@login_required(login_url="login/")
@csrf_exempt
def notification_update(request, pk):
	"""
    Modification de l'information d'une notification
    """

	obj = get_object_or_404(Notification, pk=pk)
	if request.method == 'POST':
		form = NotificationForm(request.POST, instance=obj)
	else:
		form = NotificationForm(instance=obj)

	return save_notification_form(request, form, NotificationTemplate.update, 'update')

@login_required(login_url="login/")
@csrf_exempt
def notification_open(request, pk):
	"""
	Modification de l'information d'une notification
	"""
	obj = get_object_or_404(Notification, pk=pk)
	if request.method == 'POST':
		form = NotificationForm(request.POST, instance=obj)
	else:
		form = NotificationForm(instance=obj)

	context = {'obj': obj,}

	data = dict()
	data['html_form'] = render_to_string(NotificationTemplate.update, context, request=request)

	return JsonResponse(data)

#----------------------------------------------------------------

def save_notification_form(request, form, template_name, action):
	"""
	Sauvegarde des informations d'une notification
	"""
	data = dict()
	if request.method == 'POST':		
		if form.is_valid():			
			OperationsHelpers.execute_action(request, action, form)
			
			lst = PaginatorHelpers.get_list_paginator(request, Notification) 
			
			data['form_is_valid'] = True
			data['html_content_list'] = render_to_string(NotificationTemplate.list, {'lst': lst})
		else:
			return ErrorsHelpers.show(request, form)

	context = {'form': form}
	data['html_form'] = render_to_string(template_name, context, request=request)
	
	return JsonResponse(data)