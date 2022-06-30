from django.http import JsonResponse, HttpResponse
from django.template.loader import render_to_string

class ErrorsHelpers():
	"""
	Cette classe effectue la gestion des erreurs ...
	"""
	def show(request, form):
		data = dict()		
		context = {'form': form}
		data['html_form'] = render_to_string("error.html", context, request=request)
		
		return JsonResponse(data)
	
	def show_message(request, message):
		data = dict()		
		context = {'message': message}
		data['error'] = True
		data['message'] = message
		data['html_form'] = render_to_string("error_message.html", context, request=request)
		data['url_redirect'] = request.session['url_list']
		
		return JsonResponse(data)
