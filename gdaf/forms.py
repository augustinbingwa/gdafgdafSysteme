from django.contrib.auth.forms import AuthenticationForm
from django import forms

#Formulaire du Login (Front End)
class LoginForm(AuthenticationForm):
    username = forms.CharField(
        label="Utilisateur", 
        max_length=30, 
        widget=forms.TextInput(attrs={'class': 'form-control', 'name': 'username', 'placeholder':"Nom d'utilisateur"}))

    password = forms.CharField(
        label="Mot de passe",
        max_length=30, 
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'name': 'password', 'placeholder':'Mot de passe'}))
