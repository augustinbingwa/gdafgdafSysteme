from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.template.loader import render_to_string
#from django.views.decorators.csrf import csrf_exempt
#from django.utils.module_loading import import_string
from django.contrib.auth.models import User

from mod_helpers.models import UserProfile
from mod_helpers.templates import USerProfileTemplate

from django.utils import timezone

#------------------------------------------------------------
def show_user_profile(request):
	"""
	View profile
	"""
	obj = get_object_or_404(UserProfile, user=request.user)
	context = {'obj': obj}
	data = dict()
	data['html_form'] = render_to_string(USerProfileTemplate.show, context, request=request)

	return JsonResponse(data)