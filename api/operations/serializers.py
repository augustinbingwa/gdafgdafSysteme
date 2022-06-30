from rest_framework import serializers
from mod_parametrage.models import ReportFileupload

class ReportFileuploadSerializer(serializers.ModelSerializer):
  class Meta:
    model = ReportFileupload
    fields = ('file', 'agence', 'timestamp')