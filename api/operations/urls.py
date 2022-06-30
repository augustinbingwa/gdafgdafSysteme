from django.urls import path
from .views import *

urlpatterns = [
    path('upload_report/', UploadReportFileView.as_view(), name='UploadReportFileView'),
    path('update_upload_report/', UpdateUploadReportFileView.as_view(), name='UpdateUploadReportFileView'),
]