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
from mod_finance.models import NoteImposition, NoteImpositionPaiement, Agence,AvisImposition

# from apps.payments.models import NoteImpositionPaymentStatement
from api.core.renderers import ObjectJSONRenderer
from api.payments import error_codes

from api import serializers  # , models
from api.permissions import UserHasAgencePermission
from api.payments.utils import (
    gdaf_filters,
    ni_lookups,
    ni_form_utils,
    ni_periode,
    ni_gdaf,
)


# logger = logging.getLogger(__name__)
# IHELA_AGENCE_MAPPING = getattr(settings, "IHELA_AGENCE_MAPPING", {})


class NoteImpositionAPIView(APIView):
    # serializer_class = serializers.RechercheNoteSerializer
    permission_classes = (permissions.IsAuthenticated, UserHasAgencePermission)

    @swagger_auto_schema(
        # request_body=serializers.RechercheNoteSerializer,
        responses={200: serializers.NoteImpositionSerializer}
    )
    def post(self, request, ni_type):
        # serializer = self.serializer_class(data=self.request.data)
        serializer = self.request.data
        # serializer.is_valid(raise_exception=True)
        lookup_query = Q()
        return_none_query = False
        INVALID_DATA_MSG = "Données invalides"
        detected_invalid_data = False
        note_imposition = serializer.get("note_imposition", None)
        contribuable = serializer.get("contribuable", None)
        # logger.info("NOTE IMPOSITION LOOKUP : %s" % ni_type)
        # Lookup Note Imposition reference
        if note_imposition:
            lookup_query = lookup_query & Q(reference__iexact=serializer["note_imposition"])

        # Lookup Contribuable
        if contribuable:
            pp = PersonnePhysique.objects.filter(
                identite_numero__iexact=serializer["contribuable"]
            )
            if pp.exists():
                contribuable_matricule = pp.first().matricule
            else:
                contribuable_matricule = serializer["contribuable"]
            lookup_query = lookup_query & (
                Q(contribuable__matricule__iexact=contribuable_matricule)
            )

        ni_lookups_query, detected_invalid_data = ni_lookups.get_note_imposition_lookup(
            ni_type, serializer, note_imposition, contribuable
        )
        lookup_query = lookup_query & ni_lookups_query

        # logger.debug("LOOKUP : %s" % lookup_query)

        # If data are invalid, just return 400
        # Invalid data is to be returned if variable is True
        if detected_invalid_data:
            return Response(
                {"detail": INVALID_DATA_MSG, "success": False},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # contribuable = lookup_obj.contribuable
        all_notes_imposition = NoteImposition.objects.filter(lookup_query).order_by(
            "annee", "entity"
        )

        # Impot foncier has further logics verifications
        # We cannot generates the next note automatically
        for note_ in all_notes_imposition:
            if note_.entity != enums.ENTITY_IMPOT_FONCIER:
                # for annee_iter in range(timezone.now().year - note_.annee + 1):
                #     annee_selectionnee = note_.annee + annee_iter
                # Si paye et pas de note suivante
                annee_selectionnee = note_.annee
                ni_form_utils.bulk_generate_consecutive_notes(
                    self.request.user,
                    note_,
                    gdaf_filters.get_entity_obj(note_),
                    annee_selectionnee,
                )
        # If there is no note, just generate the next
        # TODO : Ask how it cn be done
        if not all_notes_imposition.exists():
            pass
            # ni_form_utils.

        # logger.debug(
        #     "All notes Before relookup : %s : %s" % (lookup_query, all_notes_imposition)
        # )
        # Re-LookUp
        all_notes_imposition = (
            NoteImposition.objects.filter(lookup_query)
            .filter(taxe_montant__gt=F("taxe_montant_paye"))
            .order_by("annee", "entity")
        )

        if ni_type == "transport":
            stationement_notes = all_notes_imposition.filter(
                entity=enums.ENTITY_DROIT_STATIONNEMENT
            )
            carte_notes = all_notes_imposition.filter(
                entity=enums.ENTITY_VEHICULE_ACTIVITE
            )

            # If there is carte municipale,
            # Return the only card that is unpaid
            # The card must be paid before other stationnement
            if carte_notes.exists():
                for stationnement in stationement_notes:
                    current_period_carte = ni_periode.get_current_period(
                        carte_notes.first().periode.periode_type, date=None
                    )
                    current_carte_lookup = ni_periode.get_month_gte_trimestre_qs(
                        stationnement.periode
                    )
                    current_carte_municipale_exists = False

                    if current_carte_lookup:
                        current_carte_municipale = all_notes_imposition.filter(
                            Q(annee=stationnement.annee) & current_carte_lookup
                        )

                        current_carte_municipale_exists = (
                            current_carte_municipale.exists()
                        )
                        if current_carte_municipale_exists:
                            all_notes_imposition = current_carte_municipale

                    # S'il y a au moins une note de stationnement,
                    # On arrete la boucle
                    if not current_carte_lookup or not current_carte_municipale_exists:
                        break

        # logger.debug("All notes : %s" % all_notes_imposition)

        ni_serializer_context = {"request": request}

        if all_notes_imposition.exists():
            return Response(
                {
                    "success": True,
                    "response_data": serializers.NoteImpositionSerializer(
                        all_notes_imposition, context=ni_serializer_context, many=True
                    ).data,
                    "response_message": _("Success"),
                    "response_code": "00",
                }
            )
        else:
            return Response(
                {
                    "success": False,
                    "response_data": [],
                    "response_message": _("No element found"),
                    "response_code": "01",
                }
            )

        # mairie = ni_gdaf.GDAFAPICall()

        # # returned_status, returned_data = mairie.creation_contribuable_physique_request(
        # #     self.request.data
        # # )
        # returned_status, returned_data = mairie.get_note_imposition_request(
        #     ni_type, self.request.data
        # )

        # return Response(returned_data, status=returned_status)

class AvisImpositionAPIView(APIView):
    permission_classes = (permissions.IsAuthenticated, UserHasAgencePermission)
    @swagger_auto_schema(
        responses={200: serializers.AvisImpositionSerializer}
    )
    def post(self, request, ni_type):
        serializer = self.request.data
        lookup_query = Q()
        INVALID_DATA_MSG = "Données invalides"

        avis_imposition = serializer.get("avis_imposition", None)
        contribuable = serializer.get("contribuable", None)

        # logger.info("AVIS IMPOSITION LOOKUP : %s" % ni_type)
        print(avis_imposition)

        # Lookup Avis Imposition reference
        if avis_imposition:
            lookup_query = lookup_query & Q(reference__iexact=avis_imposition)

        # Lookup Contribuable
        if contribuable:
            pp = PersonnePhysique.objects.filter(
                identite_numero__iexact=serializer["contribuable"]
            )
            if pp.exists():
                contribuable_matricule = pp.first().matricule
            else:
                contribuable_matricule = serializer["contribuable"]
            lookup_query = lookup_query & (Q(contribuable__matricule__iexact=contribuable_matricule))

        ni_lookups_query, detected_invalid_data = ni_lookups.get_avis_imposition_lookup(
            ni_type, serializer, avis_imposition, contribuable
        )
        lookup_query = lookup_query & ni_lookups_query

        print(ni_lookups_query, detected_invalid_data)
        print(lookup_query)

        # logger.debug("LOOKUP : %s" % lookup_query)

        # If data are invalid, just return 400
        # Invalid data is to be returned if variable is True
        if detected_invalid_data:
            return Response(
                {"detail": INVALID_DATA_MSG, "success": False},
                status=status.HTTP_400_BAD_REQUEST,
            )

        all_avis_imposition = AvisImposition.objects.filter(lookup_query).order_by("entity")
        print(all_avis_imposition)
        if not all_avis_imposition.exists():
            pass

        # logger.debug("All avis Before relookup : %s : %s" % (lookup_query, all_avis_imposition))

        # all_avis_imposition = (AvisImposition.objects.filter(lookup_query).filter(taxe_montant__gt=F("montant_total")).order_by("entity"))
        # print(all_avis_imposition,lookup_query,F("montant_total")).order_by("entity"))

        # logger.debug("All avis : %s" % all_avis_imposition)

        ni_serializer_context = {"request": request}

        if all_avis_imposition.exists():
            return Response(
                {
                    "success": True,
                    "response_data": serializers.AvisImpositionSerializer(all_avis_imposition, context=ni_serializer_context, many=True).data,
                    "response_message": _("Success"),
                    "response_code": "00",
                }
            )
        else:
            return Response(
                {
                    "success": False,
                    "response_data": [],
                    "response_message": _("No element found"),
                    "response_code": "01",
                }
            )

class NoteImpositionPaymentAPIView(APIView):
    permission_classes = (permissions.IsAuthenticated, UserHasAgencePermission)
    def post(self, request, ni_type):
        """
        Note imposition payment

        Data : {'reference': 'NI....', 'reference_banque': '...', 'montant': '...', 'description_banque': '...'}
        """

        # serializer = self.serializer_class(data=self.request.data)
        # serializer = self.request.data
        # serializer.is_valid(raise_exception=True)
        lookup_query = Q()
        return_none_query = False
        INVALID_DATA_MSG = "Données invalides"

        noteimposition_data = self.request.data
        # ihela_payment_id = serializer.get("ihela_pay_id", "NoID")
        returned_data = {
            "success": False,
            "response_data": {
                "menu": "note_paiement",
                "notes": noteimposition_data,
                "payment": [],
            },
            "response_code": error_codes.GENERIC_ERROR_CODE,
        }
        returned_status = status.HTTP_200_OK
        detected_invalid_data = False
        # logger.info("NOTE IMPOSITION PAYMENT : %s" % ni_type)
        # logger.debug("PAYMENT DATA : %s" % request.data)

        payment_agence_bank = Agence.get_for_user(self.request.user)

        if not payment_agence_bank:
            return Response(
                {
                    "success": False,
                    "response_code": "403",
                    "response_message": _("You are not allowed to access this service"),
                    "response_data": None,
                }
            )

        # if noteimposition_data.get("reference", None):
        #
        #     etat,note = get_last_note(noteimposition_data["reference"])
        #     print(etat,note,'***********************************************************************************************')
        #     if etat == True:
        #         returned_data["response_message"] = _("Vous devez paie d'abord la note :"+ note)
        #         return Response(returned_data, status=returned_status)
        #     else:
        #         returned_data["success"] = False
        #         returned_data["response_data"] = None
        #         returned_data["response_message"] = _("Invalid references given")
        #         returned_data["response_code"] = INVALID_DATA_ERROR_CODE

        # Pay the notes here
        # And do all the stuff before return the data
        if noteimposition_data.get("reference", None) and noteimposition_data.get("reference_banque", None):
            print(noteimposition_data,'***********************************************************************************************')
            try:                note_imposition = (
                    NoteImposition.objects.filter(
                        taxe_montant__gt=F("taxe_montant_paye")
                    )
                    .order_by("entity")
                    .get(reference=noteimposition_data["reference"])
                )
            except NoteImposition.DoesNotExist:
                returned_data["success"] = False
                returned_data["response_data"] = {
                    "reference": noteimposition_data["reference"]
                }
                returned_data["response_message"] = _(
                    "Could not find a payable element"
                )
                returned_data["response_code"] = error_codes.NOT_FOUND_ERROR_CODE

                return Response(returned_data, status=returned_status)

            note_montant = Decimal(str(noteimposition_data.get("montant", 0)))
            montant_requis = (
                note_imposition.taxe_montant - note_imposition.taxe_montant_paye
            )
            montant_excedant = 0
            montant_payable = note_montant
            if montant_requis < note_montant:
                montant_excedant = note_montant - montant_requis
                montant_payable = montant_requis

            # Verification :
            # We complete the reference from the bank
            if (
                noteimposition_data["reference_banque"]
                not in noteimposition_data["description_banque"]
            ):
                bank_description = "%s %s" % (
                    noteimposition_data["description_banque"],
                    noteimposition_data["reference_banque"],
                )

            if note_imposition.libelle not in noteimposition_data["description_banque"]:
                bank_description = "%s %s" % (
                    note_imposition.libelle,
                    noteimposition_data["description_banque"],
                )

            # Verification :
            # We check the amount
            if not montant_payable or montant_payable <= 0:
                returned_data["success"] = False
                returned_data["response_data"] = None
                returned_data["response_message"] = _("Invalid amount")
                returned_data["response_code"] = error_codes.INVALID_AMOUNT_ERROR_CODE

                # We break verifications
                return Response(returned_data, status=returned_status)

            # Verification :
            # We check if there is an existant payment with same reference for the bank
            if NoteImpositionPaiement.objects.filter(
                agence=payment_agence_bank,
                ref_paiement=noteimposition_data["reference_banque"],
            ).exists():
                returned_data["success"] = False
                returned_data["response_data"] = None
                returned_data["response_message"] = _(
                    "Payment with the same reference exists for the same bank"
                )
                returned_data[
                    "response_code"
                ] = error_codes.EXISTING_REFERENCE_ERROR_CODE

                # We break verifications
                return Response(returned_data, status=returned_status)

            # statement = NoteImpositionPaymentStatement.objects.create(
            #     note_imposition=note_imposition.pk,
            #     note_type=NoteImpositionPaymentStatement.TAXE,
            #     user=self.request.user,
            #     ref_paiement=noteimposition_data["reference_banque"],
            #     # agence=Agence.objects.get(
            #     #     code="15"
            #     # ).pk,  # TODO: Get Agence from API.
            #     agence=IHELA_AGENCE_MAPPED,
            #     date_paiement=noteimposition_data["date"],
            #     montant_tranche=montant_payable,
            #     bank_name=noteimposition_data["bank_name"],
            #     bank_user=noteimposition_data["bank_user"],
            #     bank_description=bank_description,
            #     # ihela_id=ihela_payment_id,
            # )

            note_imposition_payment = NoteImpositionPaiement.objects.create(
                note_imposition=note_imposition,
                # agence=Agence.objects.get(
                #     code="15"
                # ),  # TODO: Get Agence from API.
                agence=payment_agence_bank,
                ref_paiement=noteimposition_data["reference_banque"],
                date_paiement=noteimposition_data.get("date", timezone.now()),
                montant_tranche=montant_payable,
                montant_excedant=montant_excedant,
                # note=noteimp["note"],
                # user_note=self.request.user,
                # date_note=timezone.now()
                user_create=self.request.user,
                user_validate=self.request.user,
                date_validate=timezone.now(),
            )

            # Pay the note
            note_imposition.taxe_montant_paye = (
                note_imposition.taxe_montant_paye + montant_payable
            )

            if montant_excedant > 0:
                note_imposition.montant_excedant = montant_excedant

            note_imposition.date_validate = timezone.now()
            note_imposition.user_validate = self.request.user
            note_imposition.save()

            # Generate File
            note_imposition_payment.fichier_paiement = None
            note_imposition_payment.save()

            # Save the statement
            # statement.note_payment = note_imposition_payment.pk
            # statement.executed = True
            # statement.generate_file()
            # statement.save()

            returned_data["success"] = True
            returned_data["response_data"] = {
                "reference": note_imposition.reference,
                "montant_restant": note_imposition.taxe_montant
                - note_imposition.taxe_montant_paye
                if note_imposition.taxe_montant > note_imposition.taxe_montant_paye
                else 0,
                "montant_paye": montant_payable,
                "montant_excedant": montant_excedant,
                "description": bank_description,
            }
            returned_data["response_message"] = _("Paid")
            returned_data["response_code"] = error_codes.SUCCESS_CODE
        else:
            returned_data["success"] = False
            returned_data["response_data"] = None
            returned_data["response_message"] = _("Invalid references given")
            returned_data["response_code"] = INVALID_DATA_ERROR_CODE

        # logger.debug("All notes : %s" % noteimposition_data)

        return Response(returned_data, status=returned_status)

class AvisImpositionPaymentAPIView(APIView):
    permission_classes = (permissions.IsAuthenticated, UserHasAgencePermission)
    def post(self, request, ni_type):
        """
        Avis imposition payment

        Data : {'reference': 'AI....', 'reference_banque': '...', 'montant': '...', 'description_banque': '...'}
        """
        avisimposition_data = self.request.data
        print(avisimposition_data)
        returned_data = {
            "success": False,
            "response_data": {
                "menu": "avis_paiement",
                "notes": avisimposition_data,
                "payment": [],
            },
            "response_code": error_codes.GENERIC_ERROR_CODE,
        }
        returned_status = status.HTTP_200_OK

        # logger.info("AVIS IMPOSITION PAYMENT : %s" % ni_type)
        # logger.debug("PAYMENT DATA : %s" % request.data)

        payment_agence_bank = Agence.get_for_user(self.request.user)
        print(payment_agence_bank)

        if not payment_agence_bank:
            return Response(
                {
                    "success": False,
                    "response_code": "403",
                    "response_message": _("You are not allowed to access this service"),
                    "response_data": None,
                }
            )

        # Pay the avis here
        # And do all the stuff before return the data
        if avisimposition_data.get("reference", None) and avisimposition_data.get("reference_banque", None):
            print(avisimposition_data.get("reference", None),avisimposition_data.get("reference_banque", None))
            try:
                avis_imposition = (AvisImposition.objects.get(reference=avisimposition_data["reference"]))
                print(avis_imposition)
            except AvisImposition.DoesNotExist:
                returned_data["success"] = False
                returned_data["response_data"] = {"reference": avisimposition_data["reference"]}
                returned_data["response_message"] = _("Could not find a payable element")
                returned_data["response_code"] = error_codes.NOT_FOUND_ERROR_CODE

                return Response(returned_data, status=returned_status)

            avis_montant = Decimal(str(avisimposition_data.get("montant", 0)))
            montant_requis = (avis_imposition.taxe_montant - avis_imposition.montant_total)
            montant_excedant = 0
            montant_payable = avis_montant
            if montant_requis < avis_montant:
                montant_excedant = avis_montant - montant_requis
                montant_payable = montant_requis
            print(avis_montant,montant_requis,avis_imposition.taxe_montant,avis_imposition.montant_total)

            # Verification :
            # We complete the reference from the bank
            if avisimposition_data["reference_banque"] not in avisimposition_data["description_banque"]:
                bank_description = "%s %s" % (avisimposition_data["description_banque"],avisimposition_data["reference_banque"],)

            if avis_imposition.libelle not in avisimposition_data["description_banque"]:
                bank_description = "%s %s" % (avis_imposition.libelle,avisimposition_data["description_banque"],)

            # Verification :
            # We check the amount
            if not montant_payable or montant_payable <= 0:
                returned_data["success"] = False
                returned_data["response_data"] = None
                returned_data["response_message"] = _("Invalid amount")
                returned_data["response_code"] = error_codes.INVALID_AMOUNT_ERROR_CODE

                # We break verifications
                return Response(returned_data, status=returned_status)

            # Verification :
            # We check if there is an existant payment with same reference for the bank
            if AvisImposition.objects.filter(agence=payment_agence_bank,ref_paiement=avisimposition_data["reference_banque"], ).exists():
                returned_data["success"] = False
                returned_data["response_data"] = None
                returned_data["response_message"] = _("Payment with the same reference exists for the same bank")
                returned_data["response_code"] = error_codes.EXISTING_REFERENCE_ERROR_CODE

                # We break verifications
                return Response(returned_data, status=returned_status)



            avis_imposition_payment = AvisImposition.objects.get(id=avis_imposition.id)
            avis_imposition_payment.agence = payment_agence_bank
            avis_imposition_payment.ref_paiement = avisimposition_data["reference_banque"]
            avis_imposition_payment.date_paiement = avisimposition_data.get("date", timezone.now())
            avis_imposition_payment.montant_total = montant_payable
            if montant_excedant > 0:
                avis_imposition_payment.montant_excedant = montant_excedant
            avis_imposition_payment.save()


            returned_data["success"] = True
            returned_data["response_data"] = {
                "reference": avis_imposition.reference,
                "montant_paye": montant_payable,
                "montant_excedant": montant_excedant,
                "description": bank_description,
            }
            returned_data["response_message"] = _("Paid")
            returned_data["response_code"] = error_codes.SUCCESS_CODE
        else:
            returned_data["success"] = False
            returned_data["response_data"] = None
            returned_data["response_message"] = _("Invalid references given")
            returned_data["response_code"] = INVALID_DATA_ERROR_CODE

        # logger.debug("All Avis : %s" % avisimposition_data)

        return Response(returned_data, status=returned_status)
