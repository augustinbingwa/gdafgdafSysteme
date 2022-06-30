from django import forms

from mod_parametrage.models import Notification

class NotificationForm(forms.ModelForm):
    """date_create
    Formulaire : Notification
    """
    class Meta:
        model = Notification

        fields = ('type', 'objet', 'message', 'user_validate', )

        exclude = ('entity', 'entity_id', 'reponse', 'user_create', 'date_create', 'date_validate')

        widgets = {
            'objet': forms.TextInput(attrs={'placeholder':'Objet du message ...'}),
            'message': forms.Textarea(attrs={'rows':2, 'style':'resize:none;', 'placeholder':"Le message à envoyer ..."}),
        }

        labels = {
            "type": "Type de message",
            'objet' : 'Objet',
            'message' : 'Message',
            'user_validate' : 'Envoyé à',
        }

    def __init__(self, *args, **kwargs):
        super(NotificationForm, self).__init__(*args, **kwargs)

        #Identifiant de l'objet en cours
        self._id = int(self.instance.id or 0)
