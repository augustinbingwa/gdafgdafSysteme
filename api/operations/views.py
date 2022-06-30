from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework import status

from django.http.response import JsonResponse
from api.operations.serializers import ReportFileuploadSerializer
from mod_parametrage.models import ReportFileupload

class UploadReportFileView(APIView):
  parser_classes = (MultiPartParser, FormParser)
  def post(self, request, *args, **kwargs):
    file_serializer = ReportFileuploadSerializer(data=request.data)
    if file_serializer.is_valid():
      file_serializer.save()
      return Response(file_serializer.data, status=status.HTTP_201_CREATED)
    else:
      return Response(file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UpdateUploadReportFileView(APIView):
    parser_classes = (MultiPartParser, FormParser)
    def post(self, request, *args, **kwargs):

        agence = request.data.get("agence")
        timestamp = request.data.get("timestamp")
        # obj = ReportFileupload.objects.filter(timestamp__gte=timestamp)
        # print(obj,type(timestamp))
        try:
            obj = ReportFileupload.objects.filter(agence=agence,timestamp__gte=timestamp).first()
        except:
            return JsonResponse({'message': 'The object does not exist'}, status=status.HTTP_404_NOT_FOUND)

        file_serializer = ReportFileuploadSerializer(obj,data=request.data)
        if file_serializer.is_valid():
            file_serializer.save()
            return Response(file_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
