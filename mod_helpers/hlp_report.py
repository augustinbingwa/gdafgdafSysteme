from django.shortcuts import render
from django.http import HttpResponse
from django.template.loader import get_template
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from qr_code.qrcode.utils import QRCodeOptions

from io import BytesIO
from xhtml2pdf import pisa

class ReportHelpers():
	"""
	Géneration du template html en fichier pdf
	"""
	def render_to_pdf(template_src, context_dict={}):
		"""
		2 - Deuxième méthode
		"""
		template = get_template(template_src)
		html= template.render(context_dict)
		result = BytesIO()
		pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), result)
		
		if not pdf.err:
			return HttpResponse(result.getvalue(), content_type='application/pdf')
		
		return None #HttpResponse("Erreur de génération du fichier PDF")

	#----------------------------------------------------------------
	def Render(request, filename, context):
		"""
		Generer fichier pdf
		"""	
		#Le fichier template		
		template_html = 'reporting/%s.html' %(filename) 		
		#Render le PDF
		pdf = ReportHelpers.render_to_pdf(template_html, context)
		
		#Option du PDF
		if pdf:
			response = HttpResponse(pdf, content_type='application/pdf')
			filename_ext = "%s.pdf" %(filename)
			content = "inline; filename='%s'" %(filename_ext)
			response['Content-Disposition'] = content
			download = request.GET.get("download")
			if download:
				content = "attachment; filename='%s'" %(filename_ext)
			
			response['Content-Disposition'] = content
			
			return response

		return HttpResponse("Erreur de génération du fichier PDF")


	#----------------------------------------------------------------
	def get_qr_options():
		"""
		Inforamtions de la configurations du code QR (image)
		"""
		return QRCodeOptions(size="s", border=8, image_format='png', error_correction='L')

	#----------------------------------------------------------------
	def export_csv(queryset, filename):
		"""
		Eport des données vers un fichier CSV
		"""
		import csv
		from django.utils.encoding import smart_str
		
		# Forcer le download
		response = HttpResponse(content_type='text/csv')
		response['Content-Disposition'] = 'attachment; filename=' + filename + '.csv'
		
		# Lecure des meta data
		opts = queryset.model._meta

		# Définir le csv fichier
		writer = csv.writer(response)
		field_names = [field.name for field in opts.fields]

		# Ecrire la premère ligne avec les entête de colonnes
		writer.writerow(field_names)
		
		# Ecrire les lignes des données
		for obj in queryset:
			writer.writerow([getattr(obj, field) for field in field_names])
		
		return response

	#----------------------------------------------------------------
	def export_xls(queryset, filename):
		"""
		Eport des données vers un fichier CSV
		"""
		import xlwt
		response = HttpResponse(content_type='application/ms-excel')
		response['Content-Disposition'] = 'attachment; filename=' + filename + '.xls'
		
		wb = xlwt.Workbook(encoding='utf-8')
		ws = wb.add_sheet("Liste")
		
		row_num = 0

		font_style = xlwt.XFStyle()
		font_style.font.bold = True
		
		# Lecure des meta data
		opts = queryset.model._meta
		columns = [field.name for field in opts.fields]

		toto = len(columns)

		for col_num in range(len(columns)):
			ws.write(row_num, col_num, columns[col_num], font_style)
		
		font_style = xlwt.XFStyle()
		
		for row in queryset:
			row_num += 1
			for col_num in range(len(columns)):
				try:
					val = str(getattr(row, columns[col_num]))
					if val == 'None':
						val = ''
					else:
						if val == 'True':
							val = 1
						elif val == 'False':
							val = 0

					ws.write(row_num, col_num, val, font_style)
				except:
					continue
		
		wb.save(response)
		return response