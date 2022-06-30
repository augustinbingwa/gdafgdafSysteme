from datetime import datetime

from django.utils import timezone
from django.utils.translation import gettext as _

from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from drf_yasg.utils import swagger_serializer_method

from drf_extra_fields.fields import Base64ImageField

from mod_parametrage import enums

from mod_helpers import hlp_chrono
from mod_crm.models import PersonnePhysique, PersonneMorale
from mod_finance.models import NoteImposition,AvisImposition
from mod_parametrage.models import Commune, Zone, Quartier, Accessibilite, RueOuAvenue
from api.payments.utils import gdaf_filters as utils
from api.payments.utils import ni_form_utils, ni_periode


class NoteImpositionSerializer(serializers.ModelSerializer):
    nom = serializers.CharField(source="contribuable.nom")
    nic = serializers.CharField(source="contribuable.matricule")
    adresse = serializers.SerializerMethodField()
    periode = serializers.SerializerMethodField()
    next_periode = serializers.SerializerMethodField()
    titre = serializers.SerializerMethodField()
    montant = serializers.SerializerMethodField()
    carte = serializers.SerializerMethodField()
    carte_label = serializers.SerializerMethodField()
    libelle = serializers.SerializerMethodField()
    paye = serializers.SerializerMethodField()
    retard = serializers.SerializerMethodField()
    ni_type = serializers.SerializerMethodField()

    class Meta:
        model = NoteImposition
        fields = [
            "id",
            # "entity_id",
            # "entity",
            "reference",
            "titre",
            "nom",
            "nic",
            "adresse",
            "libelle",
            "numero_carte_physique",
            "carte",
            "carte_label",
            "taxe_montant",
            "nombre_impression",
            "periode",
            "next_periode",
            "montant",
            "taxe_montant_paye",
            "paye",
            "retard",
            "ni_type",
        ]

    def get_adresse(self, obj):
        adr = ""
        if obj.contribuable.adresse:
            adr += "%s " % obj.contribuable.adresse
        if obj.contribuable.numero_rueavenue:
            adr += "%s " % obj.contribuable.numero_rueavenue
        if obj.contribuable.numero_police:
            adr += "%s " % obj.contribuable.numero_police
        if obj.contribuable.adresse_exacte:
            adr += "%s " % obj.contribuable.adresse_exacte

        return adr

    def get_periode(self, obj):
        return "%s - %s" % (obj.periode.get_element_display(), obj.annee)

    def get_next_periode(self, obj):
        next_periode = ni_form_utils.get_next_periode_by_note(obj)
        print(next_periode.__dict__)

    def get_titre(self, obj):
        return utils.get_ni_title(obj)

    def get_libelle(self, obj):
        lib = utils.get_libelle_note_imposition(obj)
        if not lib:
            lib = obj.libelle
        return lib

    def get_montant(self, obj):
        montant = obj.taxe_montant - obj.taxe_montant_paye
        return montant

    def get_carte(self, obj):
        return utils.get_entity_reference(obj)

    def get_carte_label(self, obj):
        return utils.get_entity_label(obj)

    @swagger_serializer_method(serializer_or_field=serializers.BooleanField)
    def get_paye(self, obj):
        return obj.taxe_montant == obj.taxe_montant_paye

    @swagger_serializer_method(serializer_or_field=serializers.BooleanField)
    def get_retard(self, obj):
        # Not same year ?
        if obj.annee < timezone.now().year:
            return True
        elif obj.annee > timezone.now().year:
            return False

        # Same period type, verify the element
        current_period = ni_periode.get_current_period(
            obj.periode.periode_type, date=None
        )

        return current_period.element > obj.periode.element

    def get_ni_type(self, obj):
        return utils.get_ni_type(obj)

class AvisImpositionSerializer(serializers.ModelSerializer):
    nom = serializers.CharField(source="contribuable.nom")
    nic = serializers.CharField(source="contribuable.matricule")
    titre = serializers.SerializerMethodField()
    montant = serializers.SerializerMethodField()
    ai_type = serializers.SerializerMethodField()

    class Meta:
        model = AvisImposition
        fields = [
            "id",
            "reference",
            "titre",
            "nom",
            "nic",
            "libelle",
            "montant_total",
            "nombre_copie",
            "montant",
            "ai_type",
        ]


    def get_titre(self, obj):
        return utils.get_ai_title(obj)

    def get_montant(self, obj):
        montant = obj.taxe_montant
        return montant

    def get_ai_type(self, obj):
        return utils.get_ai_type(obj)

class PersonnePhysiqueCreateSerializer(serializers.ModelSerializer):
    # identite = serializers.ChoiceField(choices=enums.choix_identite)
    identite_file = Base64ImageField()
    photo_file = Base64ImageField()
    # identite_file = serializers.CharField(
    #     validators=[UniqueValidator(queryset=Contribuable.objects.all())]
    # )
    # nif_numero = serializers.CharField(
    #     validators=[UniqueValidator(queryset=Contribuable.objects.all())]
    # )

    class Meta:
        model = PersonnePhysique
        fields = [
            "nom",
            "adresse_exacte",
            "numero_police",
            "code_postal",
            "tel",
            "email",
            "nif_numero",
            "adresse",
            "numero_rueavenue",
            "sexe",
            "date_naiss",
            "lieu_naiss",
            "identite",
            "identite_numero",
            "identite_file",
            "photo_file",
        ]

    def create(self, validated_data):
        request = self.context.get("request")
        user = request.user

        validated_data["matricule"] = ni_form_utils.get_new_reference(
            enums.CHRONO_PERSONNE_PHYSIQUE
        )

        validated_data["user_create"] = user.gdaf_user
        validated_data["user_update"] = user.gdaf_user
        validated_data["user_validate"] = user.gdaf_user

        validated_data["date_create"] = timezone.now()
        validated_data["date_update"] = timezone.now()
        validated_data["date_validate"] = timezone.now()

        obj = super().create(validated_data)

        return obj

    def clean_nif_numero(self, nif_numero):
        """
        Validation du numero du nif, non obligatoire matricule mais UNIQUE
        """
        if nif_numero:
            if self._id > 0:
                # Mode update
                obj = Contribuable.objects.filter(nif_numero=nif_numero).exclude(
                    id=self._id
                )
            else:
                # Mode creation
                obj = Contribuable.objects.filter(nif_numero=nif_numero)
            if obj:
                raise forms.ValidationError(_("Le numéro du NIF existe déjà"))

        return nif_numero

    # def clean(self):
    #     """
    #     Validations des champs spécifique
    #     """
    #     # Validation du nom
    #     nom = str(self.cleaned_data.get("nom")).strip()
    #     if not is_alpha_only(nom):
    #         raise forms.ValidationError(_("Le nom doit être en lettre uniquement."))
    #     if len(nom) < 4:
    #         raise forms.ValidationError(_("Nom trop court. Au moins 4 caractères."))

    #     # Validation de la date de naissance
    #     date_naiss = self.cleaned_data.get("date_naiss")

    #     if not is_date_valid(date_naiss):
    #         raise forms.ValidationError(_("Date de naissance invalide."))

    #     # Validation de la date de naissance  (minimum 16 ans)
    #     age = datetime.now().year - date_naiss.year
    #     if age < 16:
    #         raise forms.ValidationError(
    #             _("La date de naissance minimale est de 16 ans.")
    #         )

    #     # Validation deu code postal (en chiffre uniquement), facultatif
    #     code_postal = self.cleaned_data.get("code_postal")
    #     if code_postal:
    #         if not is_number_only(str(code_postal).strip()):
    #             raise forms.ValidationError(
    #                 _("Le code postal doit être en chiffre uniquement.")
    #             )

    #     # Validation de d'adresse email, facultatif
    #     email = self.cleaned_data.get("email")
    #     if email:
    #         if not is_email_valid(email):
    #             raise forms.ValidationError(_("Addresse email invalide."))

    #     # Validation du numéro de tél, facultatif
    #     tel = self.cleaned_data.get("tel")
    #     if tel:
    #         if not is_phone_valid(tel):
    #             raise forms.ValidationError(_("Numéro de téléphone invalide."))

    #     # Validation des adresses (Minimun une adresse doit être indiquée)
    #     adresse_exacte = self.cleaned_data.get("adresse_exacte")
    #     adresse = self.cleaned_data.get("adresse")
    #     numero_rueavenue = self.cleaned_data.get("numero_rueavenue")

    #     if adresse_exacte is None and adresse is None:
    #         raise forms.ValidationError(_("Veuillez indiquer l'adresse du domicile."))

    #     if adresse and numero_rueavenue:
    #         if not is_rue_avenue_exists(adresse, numero_rueavenue):
    #             raise forms.ValidationError(
    #                 _("Cette rue-avenue n'existe pas pour l'adresse seléctionnée")
    #             )

    #     return self.cleaned_data

class CommuneSerializer(serializers.ModelSerializer):
    class Meta:
        model = Commune
        fields = "__all__"

class ZoneSerializer(serializers.ModelSerializer):
    commune = CommuneSerializer()
    nom_complet = serializers.SerializerMethodField()

    class Meta:
        model = Zone
        fields = "__all__"

    def get_nom_complet(self, obj):
        return "%s (%s, %s)" % (obj.nom, obj.commune.nom)

class QuartierSerializer(serializers.ModelSerializer):
    zone = ZoneSerializer()
    nom_complet = serializers.SerializerMethodField()

    class Meta:
        model = Quartier
        fields = "__all__"

    def get_nom_complet(self, obj):
        return "%s (%s, %s)" % (obj.nom, obj.zone.nom, obj.zone.commune.nom)

class RueOuAvenueSerializer(serializers.ModelSerializer):
    accessibilite = serializers.SlugRelatedField(
        slug_field="nom", queryset=Accessibilite.objects.all()
    )
    zone = ZoneSerializer()
    nom_complet = serializers.SerializerMethodField()

    class Meta:
        model = RueOuAvenue
        fields = "__all__"

    def get_nom_complet(self, obj):
        return "%s (%s, %s)" % (obj.nom, obj.zone.nom, obj.zone.commune.nom)

class PersonnePhysiqueSerializer(serializers.ModelSerializer):
    identite_file = Base64ImageField()
    photo_file = Base64ImageField()

    adresse = QuartierSerializer()
    numero_rueavenue = RueOuAvenueSerializer()

    class Meta:
        model = PersonnePhysique
        exclude = [
            "date_update",
            "user_create",
            "user_validate",
            "user_update",
            "user_note",
        ]
