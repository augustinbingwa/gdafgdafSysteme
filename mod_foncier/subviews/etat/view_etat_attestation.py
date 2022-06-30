from mod_foncier.submodels.model_foncier_expertise import FoncierExpertise
from mod_helpers.hlp_operations import OperationsHelpers
from mod_helpers.hlp_report import ReportHelpers
#Attestation parcelle
def attestation_parcelle_pdf(request, pk):
	obj = FoncierExpertise.objects.filter(parcelle_id=pk)[0]
	#action print
	OperationsHelpers.execute_action_print(request, obj)	
	filename = 'attestation_parcelle'
	return ReportHelpers.Render(request, filename, obj)	