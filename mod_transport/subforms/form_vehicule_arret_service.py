from django.utils.translation import gettext as _
from django import forms
from django.utils import timezone
from mod_transport.submodels.model_vehicule_arret_service import *
# from dal import autocomplete

class ArretVehiculeServiceForm(forms.ModelForm):
    numero_activite=''
    activite_id=0
    class Meta:
        model = ArretVehiculeService

        fields = ('activite', 'motif')

        exclude = ('user_arret','date_arret')

        error_messages = {
            'activite': {'required': ('activite obligatoire'),}
        }

        widgets = {
            'activite': forms.TextInput(),
        }
         
        labels = {
            "activite": "N° Activité",
            "motif": "Motif",
        }

        help_texts = {
            "activite": "Numéro de la d’activité",
            "motif": "Raison de l'arrêt de service",
        }
    def __init__(self, *args, **kwargs):
        super(ArretVehiculeServiceForm, self).__init__(*args, **kwargs)

        #Gestion de contrôles : Désactiver tous le champs de saisie si l'objet est validé
        self._id = int(self.instance.id or 0) #Identifiant de l'activité encours
        self.numero_activite = self.instance.activite.numero_activite
        self.activite_id = self.instance.activite.id

        if self._id>0:
            if self.instance.date_validate:
                self.fields['activite'].widget.attrs['disabled'] = True
                self.fields['motif'].widget.attrs['disabled'] = True


class ImageUploadArretServiceForm(forms.Form):
    """Image upload form."""
    fichier_formulaire_arret_image = forms.FileField(required=False)

class ImageUploadCarteActiviteForm(forms.Form):
    """Image upload form."""
    fichier_carte_municipale_image = forms.FileField(required=False)