from django.conf import settings
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Q

from mod_helpers.hlp_notification import NotificationHelpers
from mod_parametrage.enums import *
from mod_foncier.submodels.model_foncier_expertise import FoncierExpertise
from mod_foncier.submodels.model_foncier_parcelle import FoncierParcelle
from mod_foncier.submodels.model_foncier_caracteristique import FoncierCaracteristique
from mod_finance.models import NoteImposition
from mod_helpers.hlp_operations import OperationsHelpers
from mod_helpers.hlp_penalite import penalite
from mod_helpers.hlp_auto_genere import *
from django.utils import timezone
import time as time_module
import sched

# import threading

import time, traceback, datetime
import threading
from twisted.internet import task, reactor


# ------------------------------------------------------------------
@login_required(login_url="login/")
def home(request):
    """
    Home page : tableau de bord
    """
    # Identifier le group de l'utilisateur en cours
    query = None
    if request.user.groups.filter(name="MENU_CONTRIBUABLE").exists():
        query = Q(is_superuser=False)
    elif request.user.groups.filter(name="MENU_COMMUNICATION").exists():
        query = Q(groups__name="MENU_COMMUNICATION")
    elif request.user.groups.filter(name="MENU_IMPOSITION").exists():
        query = Q(groups__name="MENU_IMPOSITION")
    elif request.user.groups.filter(name="MENU_RECETTE").exists():
        query = Q(groups__name="MENU_RECETTE")
    elif request.user.groups.filter(name="MENU_TECHNIQUE").exists():
        query = Q(groups__name="MENU_TECHNIQUE")
    elif request.user.groups.filter(name="MENU_TRANSPORT").exists():
        query = Q(groups__name="MENU_TRANSPORT")

    if query:
        # Utilisateurs des modules pour le tableau de bord
        user_list = User.objects.filter(query).order_by("-last_login")
    else:
        user_list = User.objects.order_by("-last_login")

    # Lire les notifications
    lst_notification = NotificationHelpers.get_list(request)

    context = {
        "lst_notification": lst_notification,
        "user_list": user_list,
        "current_user": request.user,
    }
    return render(request, "home.html", context)


# -----------------------------------------------------------------

# threading.Thread(target=lambda: every(60, autoTask)).start()
# threading.Thread(target=lambda: every(5, foo)).start()
# infomairie@Mairie#257
# ------------------------------------------------------------------
@login_required(login_url="login/")
def dashboard_contribuable(request):
    """
    Home page : tableau de bord
    """
    # Utiisateurs des modules pour le tableau de bord
    user_list = User.objects.filter(is_superuser=False).order_by("-last_login")

    # Lire les notifications
    lst_notification = NotificationHelpers.get_list(request)

    context = {
        "lst_notification": lst_notification,
        "user_list": user_list,
        "current_user": request.user,
    }

    return render(request, "contribuable/dashboard_contribuable.html", context)


# ------------------------------------------------------------------
@login_required(login_url="login/")
def dashboard_communication(request):
    """
    Home page : tableau de bord
    """
    # Utiisateurs des modules pour le tableau de bord
    user_list = User.objects.filter(groups__name="MENU_COMMUNICATION").order_by(
        "-last_login"
    )

    # Lire les notifications
    lst_notification = NotificationHelpers.get_list(request)

    context = {
        "lst_notification": lst_notification,
        "user_list": user_list,
        "current_user": request.user,
    }

    return render(request, "communication/dashboard_communication.html", context)


# ------------------------------------------------------------------
@login_required(login_url="login/")
def dashboard_imposition(request):
    """
    Home page : tableau de bord
    """
    # Utiisateurs des modules pour le tableau de bord
    user_list = User.objects.filter(groups__name="MENU_IMPOSITION").order_by(
        "-last_login"
    )

    # Lire les notifications
    lst_notification = NotificationHelpers.get_list(request)

    context = {
        "lst_notification": lst_notification,
        "user_list": user_list,
        "current_user": request.user,
    }

    return render(request, "imposition/dashboard_imposition.html", context)


# ------------------------------------------------------------------
@login_required(login_url="login/")
def dashboard_recette(request):
    """
    Home page : tableau de bord
    """
    # Utiisateurs des modules pour le tableau de bord
    user_list = User.objects.filter(groups__name="MENU_RECETTE").order_by("-last_login")

    # Lire les notifications
    lst_notification = NotificationHelpers.get_list(request)

    context = {
        "lst_notification": lst_notification,
        "user_list": user_list,
        "current_user": request.user,
    }

    return render(request, "recette/dashboard_recette.html", context)


# ------------------------------------------------------------------
@login_required(login_url="login/")
def dashboard_technique(request):
    """
    Home page : tableau de bord
    """
    # Utiisateurs des modules pour le tableau de bord
    user_list = User.objects.filter(groups__name="MENU_TECHNIQUE").order_by(
        "-last_login"
    )

    # Lire les notifications
    lst_notification = NotificationHelpers.get_list(request)

    context = {
        "lst_notification": lst_notification,
        "user_list": user_list,
        "current_user": request.user,
    }

    return render(request, "technique/dashboard_technique.html", context)


# ------------------------------------------------------------------
@login_required(login_url="login/")
def dashboard_transport(request):
    """
    Home page : tableau de bord
    """
    # Utiisateurs des modules pour le tableau de bord
    user_list = User.objects.filter(groups__name="MENU_TRANSPORT").order_by(
        "-last_login"
    )

    # Lire les notifications
    lst_notification = NotificationHelpers.get_list(request)

    context = {
        "lst_notification": lst_notification,
        "user_list": user_list,
        "current_user": request.user,
    }

    return render(request, "transport/dashboard_transport.html", context)


# ------------------------------------------------------------------
def error_404(request):
    return render(request, "404.html", status=404)


# ------------------------------------------------------------------
def error_500(request):
    return render(request, "500.html", status=500)


def every(delay, task):
    next_time = time.time() + delay
    while True:
        time.sleep(max(0, next_time - time.time()))
        try:
            task()
        except Exception:
            traceback.print_exc()

        next_time += (time.time() - next_time) // delay * delay + delay


# def runjob():
#     autogenere_note_impot()
#
#
# if getattr(settings, "ACTIVATE_TWISTED_THREAD", True):
#     threading.Thread(target=lambda: every(1, runjob)).start()
