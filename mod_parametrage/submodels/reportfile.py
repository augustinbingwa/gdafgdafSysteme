from django.db import models
from mod_finance.models import Agence
from mod_helpers.hlp_paths import PathsHelpers

def path_fichier_rappot_banque(instance, filename):
	return PathsHelpers.path_and_rename(instance, filename, PathsHelpers.REPORT_BANK_FILE)

class ReportFileupload(models.Model):
    file = models.FileField(upload_to=path_fichier_rappot_banque,blank=False, null=False)
    agence = models.ForeignKey(Agence, on_delete=models.CASCADE, null=True, blank=True)
    timestamp = models.DateField(auto_now_add=True)

    class Meta:
        ordering = ('-id',)

    def __str__(self):
        return str(self.file)
