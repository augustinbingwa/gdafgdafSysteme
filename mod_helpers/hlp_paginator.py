from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

class PaginatorHelpers():
	
	pageSize = 15 #Nombre de ligne par page par défaut
	
	def get_list(request, entity, order_term):
		lst = entity.objects.all().order_by(order_term)
		return lst

	def get_list_entity_filter(request, entity_filter):
		lst = entity_filter
		return lst

	def get_list_paginator(request, entity, order_term = None):
		if order_term:
			obj_list = entity.objects.all().order_by(order_term)
		else:
			obj_list = entity.objects.all()
		
		page = request.GET.get('page', 1)
		paginator = Paginator(obj_list, PaginatorHelpers.pageSize)
		
		try:
			lst = paginator.page(page)
		except PageNotAnInteger:
			lst = paginator.page(1)
		except EmptyPage:
			lst = paginator.page(paginator.num_pages)    
		
		return lst

	#Paginator pour des listes filtrées
	def get_list_paginator_entity_filter(request, entity_filter):
		obj_list = entity_filter
		page = request.GET.get('page', 1)
		paginator = Paginator(obj_list, PaginatorHelpers.pageSize)

		try:
			lst = paginator.page(page)
		except PageNotAnInteger:
			lst = paginator.page(1)
		except EmptyPage:
			lst = paginator.page(paginator.num_pages)

		return lst
