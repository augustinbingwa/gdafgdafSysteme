import logging
import requests

from django.conf import settings
from django.utils.translation import gettext as _

ETAT_CIVIL_URL = getattr(
    settings, "ETAT_CIVIL_URL", "http://192.168.1.202/formation/module2/api/"
)
ETAT_CIVIL_USER = getattr(settings, "ETAT_CIVIL_USER", "apicivilbase")
ETAT_CIVIL_PASSWORD = getattr(settings, "ETAT_CIVIL_PASSWORD", "@2020_2016@")
logger = logging.getLogger(__name__)


class EtatCivilAPI:
    def __init__(self, fetch_token=True):
        self.token = None
        if fetch_token:
            self.get_token()

    def get_token(self):
        SUCCESS_CODE = 1
        req = requests.get(
            ETAT_CIVIL_URL,
            params={"token": 0, "ident": ETAT_CIVIL_USER, "pass": ETAT_CIVIL_PASSWORD},
        )

        logger.debug(req.content)

        try:
            self.token = req.json()["token"]
        except BaseException as e:
            logger.debug("Etat Civil Token ERROR : %s" % e)
            self.token = None

    def get_avis_imposition_request(self, reference_avis):
        SUCCESS_CODE = 3
        if not self.token:
            return 401, {"error": "Authentication is required in Mairie."}

        req = requests.get(
            ETAT_CIVIL_URL, params={"token": self.token, "avis": reference_avis}
        )

        try:
            received_data = req.json()

            returned_data = received_data
            returned_status = req.status_code

            if returned_status == requests.codes.ok and str(
                received_data.get("cod", None)
            ) == str(SUCCESS_CODE):
                all_documents = self.get_tarif(get_raw=True, ignore_status=True) or {}

                print(all_documents, received_data.get("typdoc", "fake"))
                chosen_doc = all_documents.get(
                    str(received_data.get("typdoc", "fake")), {"2": ""}
                )

                returned_data = {
                    "id": reference_avis,
                    "titre": "%s Note imposition N# %s"
                    % (chosen_doc["2"], reference_avis),
                    "document_type": received_data.get("typdoc", None),
                    "quantite": received_data.get("qt", 0),
                    "montant": received_data.get("prixt", 0),
                    "reference": received_data.get("avis", None),
                    "ni_type": "etat-civil",
                }
            else:
                logger.debug("Etat Civil Request ERROR : %s" % received_data)
                returned_data = {"error": "Invalid data received"}

            return (returned_status, returned_data)
        except BaseException as e:
            logger.debug("Etat Civil Request ERROR : %s" % e)
            return 500, {"error": str(e)}

    def pay_avis_imposition(
        self,
        reference_avis,
        code_banque,
        nom_banque,
        nom_agence,
        prix_totale,
        quantite,
        reference_ext,
    ):
        SUCCESS_CODE = 5
        if not self.token:
            return 401, {"error": "Authentication is required in Mairie."}

        pay_data = {
            "token": self.token,
            "avis": reference_avis,
            "codeb": code_banque,
            "nomb": nom_banque,
            "noma": nom_agence,
            "prixt": prix_totale,
            "qt": quantite,
            "codref": reference_ext,
        }

        print("PAY :", pay_data)

        req = requests.get(ETAT_CIVIL_URL, params=pay_data)

        try:
            received_data = req.json()

            returned_data = received_data
            returned_status = req.status_code

            if returned_status == requests.codes.ok and str(
                received_data.get("cod", None)
            ) == str(SUCCESS_CODE):
                returned_data = {
                    "error": False,
                    "reference": reference_avis,
                    "bank_reference": reference_ext,
                }
            else:
                returned_data = {
                    "error": True,
                    "error_message": _("Could not pay the given note."),
                }

            return (returned_status, returned_data)
        except BaseException as e:
            logger.debug("Etat Civil Pay ERROR : %s" % e)
            return 500, {"error": str(e)}

    def creation_avis_imposition_request(
        self,
        code_document,
        quantite,
        demandeur,
        description,
        identite,
        get_raw=False,
        ignore_status=False,
    ):
        SUCCESS_CODE = 5
        if not self.token:
            return 401, {"error": "Authentication is required in Mairie."}

        req = requests.get(
            ETAT_CIVIL_URL,
            params={
                "token": self.token,
                "typdoc": code_document,
                "qt": quantite,
                "dmd": demandeur,
                "desc": description,
                "identite": identite,
            },
        )

        try:
            received_data = req.json()

            returned_data = received_data
            returned_status = req.status_code

            # If we want raw data, let's return
            # Here it is for some facilitaties
            if get_raw:
                if ignore_status:
                    return returned_data
                return returned_status, returned_data

            if returned_status == requests.codes.ok and received_data.get("avis"):
                all_documents = self.get_tarif(get_raw=True, ignore_status=True) or {}

                chosen_doc = all_documents.get(
                    str(received_data.get("typdoc", "fake")), {"2": ""}
                )

                returned_data = {
                    "reference": received_data["avis"],
                    "doctype": chosen_doc["2"],
                }
            else:
                returned_data = {}

            if ignore_status:
                return returned_data

            return (returned_status, returned_data)
        except BaseException as e:
            logger.debug("Etat Civil Creation ERROR : %s" % e)
            return 500, {"error": str(e)}

    def get_tarif(self, get_raw=False, ignore_status=False):
        SUCCESS_CODE = 1
        req = requests.get(ETAT_CIVIL_URL, params={"tarif": 0})

        try:
            received_data = req.json()

            returned_data = received_data
            returned_status = req.status_code

            # If we want raw data, let's return
            # Here it is for some facilitaties
            if get_raw:
                if ignore_status:
                    return returned_data
                return returned_status, returned_data

            if returned_status == requests.codes.ok:
                returned_data = [
                    {
                        "code": x,
                        "prix": received_data[x]["1"],
                        "title": received_data[x]["2"],
                    }
                    for x in received_data
                    if received_data[x]["2"]
                ]

                returned_data = {
                    "objects": returned_data,
                    "objectsCount": len(returned_data),
                }

            else:
                returned_data = None

            if ignore_status:
                return returned_data

            return (returned_status, returned_data)
        except BaseException as e:
            logger.debug("Etat Civil Tarif ERROR : %s" % e)
            if ignore_status:
                return {"error": str(e)}
            return 500, {"error": str(e)}
