import logging
import requests

from django.conf import settings
from django.utils.translation import gettext as _

MAIRIE_GDAF_URL = getattr(settings, "MAIRIE_GDAF_URL", "http://192.168.1.240/api/v1")
MAIRIE_GDAF_TOKEN = getattr(settings, "MAIRIE_GDAF_TOKEN", "thetoken")
logger = logging.getLogger(__name__)


class GDAFAPICall:
    def __init__(self):
        self.token = None
        self.get_token()

    def get_token(self):
        self.token = MAIRIE_GDAF_TOKEN

    def get_headers(self, headers={}):
        headersBase = {"Authorization": "Token %s" % self.token}
        headersBase.update(headers)

        return headersBase

    def get_note_imposition_request(self, ni_type, ni_data):
        if not self.token:
            return 401, {"error": "Authentication is required in Mairie."}

        ni_url = "{url}/noteimposition/{ni_type}/".format(
            url=MAIRIE_GDAF_URL, ni_type=ni_type
        )

        try:
            req = requests.post(ni_url, json=ni_data, headers=self.get_headers())
            # print(req.text)
            received_data = req.json()

            return (req.status_code, received_data)
        except BaseException as e:
            logger.error("GDAF API Request ERROR : %s" % e)
            return 500, {"error": "Internal services error."}

    def pay_note_imposition(
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

        req = requests.get(MAIRIE_GDAF_URL, params=pay_data)

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

    def creation_contribuable_physique_request(self, contribuable_data):
        if not self.token:
            return 401, {"error": "Authentication is required in Mairie."}

        ctrbl_url = "{url}/contribuable/physique/create/".format(url=MAIRIE_GDAF_URL)

        try:
            req = requests.post(
                ctrbl_url, json=contribuable_data, headers=self.get_headers()
            )
            # print(req.text)
            received_data = req.json()

            return (req.status_code, received_data)
        except BaseException as e:
            logger.error("GDAF API Request ERROR : %s" % e)
            return 500, {"error": "Internal services error."}

    def get_tarif(self, get_raw=False, ignore_status=False):
        SUCCESS_CODE = 1
        req = requests.get(MAIRIE_GDAF_URL, params={"tarif": 0})

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
