from django import forms

#----------------------------------------------------------
class NoteForm(forms.Form):
	"""
	Edition d'une note
	"""
	# La note à envoyer  par un user quelconque
	note = forms.CharField(required=True)

	# La réponse de l'utilisateur recepteur
	reponse_note = forms.CharField(required=False)

	# Demande d'annulation de validation par l'user recepteur
	demande_annulation_validation = forms.BooleanField(required=False)