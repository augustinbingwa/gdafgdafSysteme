from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.utils.safestring import mark_safe
from django.views.decorators.csrf import csrf_exempt
from django.db import transaction, IntegrityError
from mod_helpers.hlp_validators import *
from mod_helpers.hlp_paginator import PaginatorHelpers
from mod_helpers.hlp_operations import OperationsHelpers
from mod_helpers.hlp_error import ErrorsHelpers
from mod_helpers.hlp_notification import NotificationHelpers
from mod_helpers.hlp_session import SessionHelpers
from mod_activite.submodels.model_activite_arret_service import ArretService
from mod_activite.submodels.model_activite import BaseActivite
from mod_activite.subforms.form_activite_arret_service import ArretServiceForm, ImageUploadArretServiceForm
from mod_activite.templates import *

from django.utils import timezone
import datetime

# ----------------------------------------------------------------
# ---------------- CRUD Arret ervice d'activité ------------------
# ----------------------------------------------------------------
from mod_activite.templates import ArretServiceTemplate
from mod_finance.submodels.model_imposition import NoteImposition
from mod_transport.templates import VehiculeArretServiceTemplate


# ----------------------------------------------------------------
def get_list_by_criteria(request):
    """
    Renvoie la liste avec criteria
    """
    total = ArretService.objects.count

    # Initialier les variables locales, sesions via variables POST
    aa_numero_activite = SessionHelpers.init_variables(request, 'aa_numero_activite')
    aa_status = SessionHelpers.init_variables(request, 'aa_status')

    # Initialier les variables locales, sesions via variables POST pour la période
    du = SessionHelpers.init_variables(request, 'aa_du')
    au = SessionHelpers.init_variables(request, 'aa_au')
    query = None
    if aa_numero_activite:
        activite = None
        obj = BaseActivite.objects.filter(numero_activite=aa_numero_activite)
        if obj:
            for activ in obj:
                activite = activ.id

            query = SessionHelpers.get_query(query, Q(activite_id__icontains=activite))

    if aa_status == '1':  # Valide
        query = SessionHelpers.get_query(query, Q(date_arret__isnull=True))
    elif aa_status == '2':  # En attente
        query = SessionHelpers.get_query(query, Q(date_arret__isnull=False))

    # Charger la liste
    if query:
        lst = ArretService.objects.filter(query)
    else:
        lst = ArretService.objects.all()

    # Si période valide
    if is_date_fr_valid(du) and is_date_fr_valid(au):
        du = date_picker_to_date_string(du)
        au = date_picker_to_date_string(au, True)

        # if is_date_valid(du) and is_date_valid(au):
        lst = lst.filter(date_create__range=[du, au]).order_by('-date_create')

    # Renvoyer le résultat de la requete filtrée avec paginator
    return PaginatorHelpers.get_list_paginator_entity_filter(request, lst), total

# ------------------------------------------------------------
def get_context(request):
    """
    Renvoie les info du context
    """
    # Lire les notifications
    lst_notification = NotificationHelpers.get_list(request)

    # Charger la liste
    lst, total = get_list_by_criteria(request)

    # Sauvegader le context
    context = {
        'total': total,
        'lst': lst,

        'aa_numero_activite': request.session['aa_numero_activite'],
        'aa_status': request.session['aa_status'],

        'aa_du': request.session['aa_du'],
        'aa_au': request.session['aa_au'],

        'lst_notification': lst_notification,
        'user': User.objects.get(pk=request.user.id),
    }

    return context


@login_required(login_url="login/")
@csrf_exempt
def activite_arret_service_list(request):
    """
	Liste des arrêts de service d'activités
	"""
    # lst = PaginatorHelpers.get_list_paginator(request, ArretService)
    #
    # # Lire les notifications
    # lst_notification = NotificationHelpers.get_list(request)
    #
    # context = {
    #     'lst': lst,
    #     'lst_notification': lst_notification,
    # }
    request.session['url_list'] = request.get_full_path()
    return render(request, ArretServiceTemplate.index, context=get_context(request))

# ----------------------------------------------------------------
@login_required(login_url="login/")
def activite_arret_service_create(request, pk, ent):
    """
	Création d'un arrêt service activité
	"""
    obj = get_object_or_404(BaseActivite, pk=pk)
    if request.method == 'POST':
        form = ArretServiceForm(request.POST, instance=obj)
    else:
        form = ArretServiceForm(instance=obj)

    return save_arret_service_form(request, form, ArretServiceTemplate.create, ent)


# ----------------------------------------------------------------
@login_required(login_url="login/")
def activite_arret_service_update(request, pk):
    """
	Suppression d'un arrêt service activité
	"""
    obj = get_object_or_404(ArretService, pk=pk)
    dateTimeNow = datetime.datetime.now(tz=timezone.utc)
    data = dict()
    if request.method == 'POST':
        form = ArretServiceForm(request.POST, instance=obj)
        print(form.errors)
        if form.is_valid():
            obj.date_update = dateTimeNow
            obj.user_update_id = request.user.id
            obj.motif = request.POST.get('motif')
            obj.save()

            lst = PaginatorHelpers.get_list_paginator(request, ArretService)
            # Lire les notifications
            lst_notification = NotificationHelpers.get_list(request)

            context = {
                'user': User.objects.get(pk=request.user.id),
                'lst': lst,
                'lst_notification': lst_notification,
            }

            data['form_is_valid'] = True
            data['html_content_list'] = render_to_string(ArretServiceTemplate.list, context)
            data['url_redirect'] = "/activite/activite_arret_service/"
        else:
            return ErrorsHelpers.show(request, form)
    else:
        form = ArretServiceForm(instance=obj)
        context = {'form': form}
        data['html_form'] = render_to_string(ArretServiceTemplate.update, context, request=request)

    return JsonResponse(data)

# ----------------------------------------------------------------
@login_required(login_url="login/")
def activite_arret_service_delete(request, pk):
    """
    Sauvegarde des informations d'un arrêt service activité
	"""
    obj = get_object_or_404(ArretService, pk=pk)
    data = dict()
    if request.method == 'POST':
        obj.delete()

        lst = PaginatorHelpers.get_list_paginator(request, ArretService)

        # Lire les notifications
        lst_notification = NotificationHelpers.get_list(request)

        context = {
            'user': User.objects.get(pk=request.user.id),
            'lst': lst,
            'lst_notification': lst_notification,
        }

        data['form_is_valid'] = True
        data['html_content_list'] = render_to_string(ArretServiceTemplate.list, context)
    else:
        context = {'obj': obj}
        data['html_form'] = render_to_string(ArretServiceTemplate.delete, context, request=request)
    return JsonResponse(data)


# ----------------------------------------------------------------
def save_arret_service_form(request, form, template_name,ent):
    ckcf = 0
    data = dict()
    note = "<h3><b class='text-danger'>NOTE D'IMPOSITION A PAIE D'ABORD</b></h3></br>"
    dateTimeNow = datetime.datetime.now(tz=timezone.utc)
    # obj = get_object_or_404(BaseActivite, pk=form.activite_id)
    if request.method == 'POST':
        if form.is_valid():
            # OperationsHelpers.execute_action(request, action, form)
            arretActivite = ArretService()
            arretActivite.motif = request.POST.get('motif')
            arretActivite.date_create = dateTimeNow
            arretActivite.activite_id = form.activite_id
            arretActivite.user_create_id = request.user.id
            arretActivite.save()

            lst = PaginatorHelpers.get_list_paginator(request, ArretService)
            # Lire les notifications
            lst_notification = NotificationHelpers.get_list(request)

            context = {
                'user': User.objects.get(pk=request.user.id),
                'lst': lst,
                'lst_notification': lst_notification,
            }

            data['form_is_valid'] = True
            data['html_content_list'] = render_to_string(ArretServiceTemplate.list, context)
            data['url_redirect'] = "/activite/activite_arret_service/"
        else:
            return ErrorsHelpers.show(request, form)
    else:
        obj = get_object_or_404(BaseActivite, pk=form.activite_id)
        if ent != 0:
            getpayement = NoteImposition.objects.filter(entity=ent, entity_id=obj.id)
            for gtp in getpayement:
                if gtp.taxe_montant > gtp.taxe_montant_paye:
                    note += gtp.reference + '</br>'
                    ckcf = 1

        if ckcf == 0:
            context = {'form': form}
            data['html_form'] = render_to_string(template_name, context, request=request)
        else:
            massage = mark_safe(note)
            context = {'message': massage}
            data['html_form'] = render_to_string('_message_erreur.html', context, request=request)

    return JsonResponse(data)

# -------------------------------------------------------------------------------------------------------
def activite_arret_service_upload(request, pk):
    """
	Upload du fichier arret de formulaire d'activité
	"""
    obj = get_object_or_404(ArretService, pk=pk)
    data = dict()
    if request.method == 'POST':
        form = ImageUploadArretServiceForm(request.POST, request.FILES)
        if form.is_valid():
            if form.cleaned_data['fichier_formulaire_arret_image'] is not None and form.cleaned_data['fichier_carte_image'] is not None:
                obj.fichier_formulaire_arret = form.cleaned_data['fichier_formulaire_arret_image']
                obj.fichier_carte_arret = form.cleaned_data['fichier_carte_image']
                obj.save()
        return redirect('activite_arret_service_list')

        data['form_is_valid'] = False
        data['form_error'] = form.errors
    else:
        context = {'obj': obj}
        data['html_form'] = render_to_string(ArretServiceTemplate.upload, context, request=request)

    return JsonResponse(data)

# ----------------------------------------------------------------
@login_required(login_url="login/")
@csrf_exempt  # pour les methode POST qui necessite crsf_token
def activite_arret_service_validate(request):
    """
	Valider les informations d'arret  de service d'activité
	"""
    # Récuperer l'identifiant de l'activité
    try:
        with transaction.atomic():
            activite_id = request.POST["id"]
            obj = get_object_or_404(ArretService, pk=activite_id)
            user = User.objects.get(pk=request.user.id)  # get current user
            dateTimeNow = datetime.datetime.now(tz=timezone.utc)
            obj.date_arret = dateTimeNow
            obj.user_arret = user
            obj.save()

            # Mise à jour du champ "Actif " dans la base activité
            objActivite = get_object_or_404(BaseActivite, pk=obj.activite_id)
            objActivite.actif = False
            objActivite.save()

    except IntegrityError:
        return ErrorsHelpers.show_message(request, "Erreur de validation de l'arrêt servive")

    lst = PaginatorHelpers.get_list_paginator(request, ArretService)

    # Lire les notifications
    lst_notification = NotificationHelpers.get_list(request)

    context = {
        'user': User.objects.get(pk=request.user.id),
        'lst': lst,
        'lst_notification': lst_notification,
    }

    data = dict()
    data['form_is_valid'] = True
    data['html_content_list'] = render_to_string(ArretServiceTemplate.list, context)
    data['url_redirect'] = "/activite/activite_arret_service/"
    # data['html_content_list'] = render_to_string(ArretServiceTemplate.list, context)
    return JsonResponse(data)