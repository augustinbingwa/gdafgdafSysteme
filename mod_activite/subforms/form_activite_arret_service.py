from django.utils.translation import gettext as _
from django import forms
from mod_activite.submodels.model_activite_arret_service import *
from mod_activite.submodels.model_activite import BaseActivite

class ArretServiceForm(forms.ModelForm):
    class Meta:
        model = ArretService

        fields = ('activite', 'motif',)

        exclude = ('user_arret',)

        error_messages = {'motif': {'required': 'motif est obligatoire', }}

        labels = {
            "activite": "N° Activité",
            "motif": "Motif",
        }

        help_texts = {
            "activite": "Numéro de la d’activité",
            "motif": "Raison de l'arrêt de service",
        }

    def __init__(self, *args, **kwargs):
        super(ArretServiceForm, self).__init__(*args, **kwargs)

        # Gestion de contrôles : Désactiver tous le champs de saisie si l'objet est validé
        self._id = int(self.instance.id or 0)  # Identifiant de l'activité encours
        if isinstance(self.instance, ArretService):
            self.activite_id = self.instance.activite.id
            self.numero_activite = self.instance.activite.numero_activite
            self.motifup = self.instance.motif

        if isinstance(self.instance, BaseActivite):
            self.activite_id = self.instance.id
            self.numero_activite = self.instance.numero_activite



class ImageUploadArretServiceForm(forms.Form):
    """Image upload form."""
    fichier_formulaire_arret_image = forms.FileField(required=False)
    fichier_carte_image = forms.FileField(required=False)