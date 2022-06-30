from django.contrib.sessions.models import Session

class SessionHelpers():
	"""
	Initialisations des variables ocales, sessions via variables POST
	"""
	def init_variables(request, var):
		"""
		Initialisation
		"""
		if var in request.POST:
			res = request.session[var] = request.POST[var]
		else:
			if var in request.session:
				res = request.session[var]
			else:
				res = request.session[var] = ''

		return res
		
	def get_query(query, criterion):
		"""
		Gestion de query multi criterions
		"""
		if query is None:
			query = criterion
		else:
			query &= criterion

		return query