from django.utils.translation import gettext as _
from django.conf import settings
from django.utils import timezone

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from gdaf.utils import ni_etat_civil
from apps.payments.models import NoteImpositionPaymentStatement

IHELA_AGENCE_MAPPING = getattr(settings, "IHELA_AGENCE_MAPPING", {})


class DocumentTypeListAPIView(APIView):
    def get(self, request):
        etat_civil = ni_etat_civil.EtatCivilAPI(fetch_token=False)
        returned_status, returned_data = etat_civil.get_tarif()
        return Response(returned_data, status=returned_status)


class AvisImpositionAPIView(APIView):
    def get(self, request, reference):
        etat_civil = ni_etat_civil.EtatCivilAPI()

        returned_status, returned_data = etat_civil.get_avis_imposition_request(
            reference
        )
        return Response(returned_data, status=returned_status)


class AvisImpositionPayAPIView(APIView):
    def post(self, request):
        etat_civil = ni_etat_civil.EtatCivilAPI()
        request_data = self.request.data.get("noteimposition_data", {})

        returned_data = {}
        returned_status = status.HTTP_200_OK

        reference = request_data.get("note_imposition", None)
        nom_banque = request_data.get("bank_name", None)
        code_banque = request_data.get("bank_code", None)
        nom_agence = request_data.get("bank_branch_name", None)
        reference_ext = request_data.get("bank_reference", None)
        quantite = request_data.get("quantity", None)
        code_document = request_data.get("doctype", None)
        demandeur = request_data.get("client_name", None)
        prix_totale = request_data.get("amount", None)
        description = request_data.get("client_description", None)
        identite = request_data.get("client_id_card_no", None)
        bank_user = request_data.get("bank_user", None)
        bank_description = request_data.get("bank_description", None)

        # If there is no reference given, the note is created
        # Required params are code_document and quantite
        if not reference and code_document and quantite:
            new_imp_status, new_imposition = etat_civil.creation_avis_imposition_request(
                code_document, quantite, demandeur, description, identite
            )

            if new_imp_status != status.HTTP_200_OK:
                returned_data["error"] = True
                returned_data["error_message"] = _(
                    "Could not create a new document note."
                )
                reference = None
            else:
                reference = new_imposition.get("reference")
                description = new_imposition.get("doctype")

        print("ALL DATA : ", request.data)

        if reference and nom_banque and code_banque and nom_agence:
            returned_status, returned_data = etat_civil.pay_avis_imposition(
                reference_avis=reference,
                code_banque=code_banque,
                nom_banque=nom_banque,
                nom_agence=nom_agence,
                prix_totale=prix_totale,
                quantite=quantite,
                reference_ext=reference_ext,
            )

            if not returned_data.get("error", True):
                NoteImpositionPaymentStatement.objects.create(
                    note_imposition=reference,
                    note_type=NoteImpositionPaymentStatement.ETAT_CIVIL,
                    user=self.request.user,
                    ref_paiement=reference_ext,
                    # agence=models.Agence.objects.get(
                    #     code="15"
                    # ).pk,  # TODO: Get Agence from API.
                    agence=IHELA_AGENCE_MAPPING[code_banque],
                    date_paiement=timezone.now(),
                    montant_tranche=prix_totale,
                    bank_name=nom_banque,
                    bank_user=bank_user,
                    bank_description=bank_description,
                )

            returned_data["description"] = description

        else:
            returned_data = {
                "error": True,
                "error_message": _(
                    "Could not find a document note or create a new one."
                ),
            }
        return Response(returned_data, status=returned_status)
