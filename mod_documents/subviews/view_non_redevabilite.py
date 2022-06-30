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
# ----------- CRUD - Note d'imposition activité MARCHE -----------
# ----------------------------------------------------------------
def get_list_by_criteria(request):

    total = NonRedevabilite.objects.count

    reference = SessionHelpers.init_variables(request, 'pm_reference')
    libelle = SessionHelpers.init_variables(request, 'pm_libelle')

    # Définir les parametres de recherche
    query = SessionHelpers.get_query(None, Q(reference__icontains=reference))  # Premier parametre à None
    query = SessionHelpers.get_query(query, Q(libelle__icontains=libelle))

    # Charger la liste
    if query is not None:
        lst = NonRedevabilite.objects.filter(query)
    else:
        lst = NonRedevabilite.objects.all()

    # Renvoyer le résultat de la requete filtrée avec paginator
    return PaginatorHelpers.get_list_paginator_entity_filter(request, lst), total

# ----------------------------------------------------------------
def get_context(request):
    """    Renvoie les info du context
    """

    # Charger la liste
    lst, total = get_list_by_criteria(request)

    # Sauvegader le context
    context = {
        'total': total,
        'lst': lst,
    }

    return context


# ----------------------------------------------------------------
@login_required(login_url="login/")
@csrf_exempt  # pour les methode POST qui necessite crsf_token
def non_redevabilite_list(request):
    """
    Liste des notes d'impositions pour les actvités dans le marhé
    Condition : Filtrer les taxes de catégorie notes d'impositions (enum : choix_imposition = 1)
    entity = ENTITY_ACTIVITE_MARCHE
    """
    # Enregistrer l'url de la liste en cours (important pour les AJAX: Validation, Update etc )
    request.session['url_list'] = request.get_full_path()

    return render(request, AttNonRedevabiliteTemplate.index, context=get_context(request))


# ----------------------------------------------------------------
@login_required(login_url="login/")
def non_redevabilite_create(request):
    """
    Créer une note d'imposition
    entity_id = Identifiant de l'activité dans le Marché
    """
    user = User.objects.get(pk=request.user.id)

    if request.method == 'POST':
        form = NonRedevabiliteForm(request.POST)
    else:
        form = NonRedevabiliteForm()

    return save_non_redevabilite_form(request, form, AttNonRedevabiliteTemplate.create, 'create')


# ----------------------------------------------------------------
@login_required(login_url="login/")
def non_redevabilite_update(request, pk):
    """
    Modifier non-redevabilité
    """
    obj = get_object_or_404(NonRedevabilite, pk=pk)
    if request.method == 'POST':
        form = NonRedevabiliteForm(request.POST, instance=obj)
    else:
        form = NonRedevabiliteForm(instance=obj)

    return save_non_redevabilite_form(request, form, AttNonRedevabiliteTemplate.update, 'update')


# ----------------------------------------------------------------
def save_non_redevabilite_form(request, form, template_name, action, entity=None):
    """
    Sauvegarder l'objet note d'imposition
    """
    data = dict()
    if request.method == 'POST':
        if form.is_valid():
            msg = OperationsHelpers.execute_action(request, action, form, CHRONO_ATTESTATION_NON_REDEVABILITE,'reference')
            if msg:
                return ErrorsHelpers.show_message(request, msg)

            data['form_is_valid'] = True
            data['html_content_list'] = render_to_string(AttNonRedevabiliteTemplate.index)
            data['url_redirect'] = request.session['url_list']
        else:
            return ErrorsHelpers.show(request, form)

    context = {'form': form, 'entity': entity}
    data['html_form'] = render_to_string(template_name, context, request=request)

    return JsonResponse(data)

# ----------------------------------------------------------------
@csrf_exempt  # pour les methode POST qui necessite crsf_token
def ni_activite_marche_validate(request):
    """
    Valider les informations de la note
    """
    # Recupérer l'objet note d'imposition
    ID = request.POST["id"]
    obj = get_object_or_404(NoteImposition, pk=ID)

    data = dict()
    data['url_redirect'] = request.session['url_list']
    data['html_content_list'] = render_to_string(NI_ActviteMarcheTemplate.list, context)

    return JsonResponse(data)

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

#----------------------------------------------------------------
@csrf_exempt #pour les methode POST qui necessite crsf_token
def non_redevabilite_ecriture(request):
    """
    Valider les informations du non redevabilité
    TRANSACTION :
    - Note d'imposition : Taxe sur activité,
    - Note d'imposition : Droit de stationnement,
    - Avis d'imposition : Coût de la carte professionelle
    """
    # Load l'Objet VehiculeActivite
    ID = request.POST["id"]
    obj = get_object_or_404(NonRedevabilite, pk=ID)

    # Mise en garde : L'objet doit être validé
    if not obj.date_validate:
        return ErrorsHelpers.show_message(request, "Erreur, Vous devez valider cet objet avant de générer les écritures")

    # get current user
    user = User.objects.get(pk=request.user.id)

    # get current datetime
    dateTimeNow = datetime.datetime.now()

    try:
        with transaction.atomic():
            #---------------------------------------------------------------------
            #1 - Générer l'écriture de l'objet principal

            # Pour les véhicules qui n'exerce pas d'activité sous son propre compte
            #---------------------------------------------------------------------
            # 2 - Créer et Valider l'avis d'imposition pour le coût de la carte d'activité professionnelle
            # Générer le nouveau numéro chrono
            new_chrono = ChronoHelpers.get_new_num(CHRONO_AVIS_IMPOSITION)
            obj_chrono = Chrono.objects.get(prefixe = CHRONO_AVIS_IMPOSITION)
            obj_chrono.last_chrono = new_chrono
            obj_chrono.save();

            # Créer l'objet AvisImposition
            ai = AvisImposition()

            # Référence de l'avis d'imposition (chronologique)
            ai.reference = new_chrono

            # Contribuable
            ai.contribuable = obj.contribuable

            # Cout de la carte, Objet taxe (Type : Avis d'imposition)
            taxe = get_object_or_404(Taxe, pk=46)
            ai.taxe = taxe.id

            # ai.taxe_montant : Tarif de la taxe (Type : Avis d'imposition) (Formule : tarif * nombre_copie), nombre copie = 1
            ai.montant_total = taxe.tarif

            # Entity Modèle : 'VehiculeProprietaire'
            ai.entity = ENTITY_NON_REDEVABILITE

            # Identifiant de l'entity : 'VehiculeActivite'
            ai.entity_id = obj.id

            # Libellé
            ai.libelle = 'Attestation de non-redevabilité n°' + obj.reference + ',NIC du Contribuable  n°: ' + obj.contribuable.matricule

            # Traçabilité (date_create est créée depuis le model)
            ai.user_create = user

            # Sauvegarder l'avis d'imposition (coût de la carte d'activité)
            ai.save()

    except IntegrityError as e:
        return ErrorsHelpers.show_message(request,  "Erreur de génération de l'écriture " + str(e))

    data = dict()
    data['url_redirect'] = request.session['url_list']
    data['html_content_list'] = render_to_string(AttNonRedevabiliteTemplate.list, context=get_context(request))

    return JsonResponse(data)

#----------------------------------------------------------------
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