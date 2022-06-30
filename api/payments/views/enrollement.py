import logging
from decimal import Decimal

from django.db.models import F, Q
from django.utils import timezone
from django.utils.translation import gettext as _
from django.conf import settings

from rest_framework import permissions, viewsets, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.exceptions import NotFound

from drf_yasg.utils import swagger_auto_schema

from mod_parametrage import enums
from mod_crm.models import PersonnePhysique
from mod_parametrage.models import RueOuAvenue, Quartier

# from apps.payments.models import NoteImpositionPaymentStatement
from api.core.renderers import ObjectJSONRenderer

from api import serializers  # , models
from api.payments.utils import (
    gdaf_filters,
    ni_lookups,
    ni_form_utils,
    ni_periode,
    ni_gdaf,
)

logger = logging.getLogger(__name__)


class PersonnePhysiqueViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = PersonnePhysique.objects.all().select_related(
        "adresse__zone__commune__province", "numero_rueavenue__zone__commune__province"
    )
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = serializers.RueOuAvenueSerializer
    renderer_classes = [ObjectJSONRenderer]


class PersonnePhysiqueAPICreateView(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = serializers.PersonnePhysiqueCreateSerializer
    serializer_resp_class = serializers.PersonnePhysiqueSerializer

    @swagger_auto_schema(
        request_body=serializers.PersonnePhysiqueCreateSerializer,
        responses={200: serializers.PersonnePhysiqueSerializer},
    )
    def post(self, request):
        returned_data = {"error": True, "data": [], "menu": "enrollement"}
        returned_status = status.HTTP_200_OK

        serializer = self.serializer_class(
            data=request.data, context={"request": self.request}
        )
        if serializer.is_valid():
            mairie = ni_gdaf.GDAFAPICall()

            (
                returned_status,
                returned_data,
            ) = mairie.creation_contribuable_physique_request(self.request.data)
        else:
            returned_data["data"] = serializer.errors

        return Response(returned_data, status=returned_status)


class RueOuAvenueViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = RueOuAvenue.objects.all().select_related("zone__commune__province")
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = serializers.RueOuAvenueSerializer
    renderer_classes = [ObjectJSONRenderer]

    def get_queryset(self):
        qs = self.queryset

        qu = self.request.query_params.get("q")
        zone = self.request.query_params.get("zone")

        if qu and len(str(qu.split(":"))) == 2:
            q_ = qu.split(":")
            if q_[0] == "z":
                qs = qs.filter(zone__nom__icontains=q_[1])
            elif q_[0] == "c":
                qs = qs.filter(zone__commune__nom__icontains=q_[1])
            elif q_[0] == "zc" or q_[0] == "cz":
                qs = qs.filter(
                    Q(zone__commune__nom__icontains=q_[1])
                    | Q(zone__nom__icontains=q_[1])
                )
        elif qu:
            qs = qs.filter(nom__icontains=qu)

        if zone:
            qs = qs.filter(zone__id__exact=zone)

        return qs

class QuartierViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Quartier.objects.all().select_related("zone__commune__province")
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = serializers.QuartierSerializer
    renderer_classes = [ObjectJSONRenderer]

    def get_queryset(self):
        qs = self.queryset

        qu = self.request.query_params.get("q")
        zone = self.request.query_params.get("zone")

        if len(str(qu.split(":"))) == 2:
            q_ = qu.split(":")
            if q_[0] == "z":
                qs = qs.filter(zone__nom__icontains=q_[1])
            elif q_[0] == "c":
                qs = qs.filter(zone__commune__nom__icontains=q_[1])
        elif qu:
            qs = qs.filter(nom__icontains=qu)

        if zone:
            qs = qs.filter(zone__id__exact=zone)

        return qs
