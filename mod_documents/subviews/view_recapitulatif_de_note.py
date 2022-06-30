from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q, F

from mod_documents.subforms.form_non_redevabilite import NonRedevabiliteForm
from mod_helpers.hlp_paginator import PaginatorHelpers
from mod_helpers.hlp_operations import OperationsHelpers
from mod_helpers.hlp_chrono import ChronoHelpers
from mod_helpers.hlp_error import ErrorsHelpers
from mod_helpers.hlp_report import ReportHelpers
from mod_helpers.hlp_notification import NotificationHelpers
from mod_helpers.hlp_session import SessionHelpers
from mod_helpers.hlp_validators import *

from mod_documents.models import NonRedevabilite
from mod_finance.models import *
from mod_documents.forms import *
from mod_documents.templates import *

from mod_documents.models import *

from mod_parametrage.enums import *
from mod_parametrage.models import *
from datetime import datetime



# ----------------------------------------------------------------
@login_required(login_url="login/")
@csrf_exempt  # pour les methode POST qui necessite crsf_token
def recapitulatif_de_note_list(request):
    context = {'context':'context'}

    return render(request, RecapitulatifDeNoteTemplate.list ,context)


#----------------------------------------------------------------
@login_required(login_url="login/")
def non_redevabilite_pdf(request, pk):
    obj = get_object_or_404(NonRedevabilite, pk=pk)
    dateval = None
    date = datetime.today().strftime('%d/%m/%Y')

    d = datetime.today().strftime('%d')
    datevalablemonth = datetime.today().strftime('%m')
    dateyear = datetime.today().strftime('%Y')

    dep_impot = Departement.objects.get(nom='imposition')
    dep_recette = Departement.objects.get(nom='recette')
    ser_impot = Service.objects.get(nom='impots')

    fx_chef_dep_impot = Fonction.objects.get(departement_id=dep_impot.id)
    fx_chef_dep_recette = Fonction.objects.get(departement_id=dep_recette.id)
    fx_chef_sr_impot = Fonction.objects.get(service_id=ser_impot.id)

    nom_chef_dep_impot = Authority.objects.get(fonction_id=fx_chef_dep_impot.id,actif=True)
    nom_chef_dep_recette = Authority.objects.get(fonction_id=fx_chef_dep_recette.id,actif=True)
    nom_chef_sr_impot = Authority.objects.get(fonction_id=fx_chef_sr_impot.id,actif=True)

    fc_chef_dep_impot = nom_chef_dep_impot.fonction.departement.nom
    fc_chef_dep_recette = nom_chef_dep_recette.fonction.departement.nom
    fc_chef_sr_impot = str(nom_chef_sr_impot.fonction)


    if int(datevalablemonth) < 12 :
        nextmonth = int(datevalablemonth) + 1

        dateval = d+'/'+str(nextmonth)+'/'+dateyear
    else :
        nextmonth = 1
        dateval = d+'/'+nextmonth+'/'+dateyear

    user = User.objects.get(pk=request.user.id)  # get current user
    dateTimeNow = datetime.now()
    obj.user_print = user
    obj.date_print = datetime.today()
    obj.save()

    context = {'qr_options': ReportHelpers.get_qr_options(),
               'qr_data': get_qr_data(obj), 'obj': obj,
               'date': date, 'dateyear': dateyear,
               'dateval': dateval,
               'nom_chef_dep_impot':nom_chef_dep_impot,
               'nom_chef_dep_recette':nom_chef_dep_recette,
               'nom_chef_sr_impot':nom_chef_sr_impot,
               'fc_chef_dep_impot': fc_chef_dep_impot.upper(),
               'fc_chef_dep_recette': fc_chef_dep_recette.upper(),
               'fc_chef_sr_impot': fc_chef_sr_impot.upper(),
               }
    return ReportHelpers.Render(request, filename, context)

@login_required(login_url="login/")
def non_redevabilite_print(request, pk):
    obj = get_object_or_404(NonRedevabilite, pk=pk)
    date = datetime.today().strftime('%d/%m/%Y')
    dateyear = datetime.today().strftime('%Y')
    user = User.objects.get(pk=request.user.id)
    context = {'qr_options': ReportHelpers.get_qr_options(),'qr_data': get_qr_data(obj), 'obj': obj,'date': date, 'dateyear': dateyear}
    return render(request, 'reporting/attestation_de_non_redevabilite_print.html', context)


def get_qr_data(obj):
    """
    Composition des données du qr code
    """
    if isinstance(obj, NonRedevabilite):
        return 'Réf: {}\nNom: {}\nNIC: {}\nDate_De_Création:{}'.format(
            obj.reference,
            obj.contribuable.nom,
            obj.contribuable.matricule,
            obj.date_create,
        )

    return 'GDAF'