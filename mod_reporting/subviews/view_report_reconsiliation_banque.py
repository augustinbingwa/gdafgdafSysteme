from django.shortcuts import render

from django.contrib.auth.decorators import login_required
from django.db.models import Q, Sum, Func, F
from django.views.decorators.csrf import csrf_exempt

from mod_finance.models import NoteImpositionPaiement

from mod_helpers.hlp_report import ReportHelpers
from mod_helpers.hlp_session import SessionHelpers

from mod_parametrage.enums import *

from mod_helpers.hlp_validators import *

import calendar

@login_required(login_url="login/")
@csrf_exempt  # Pour les methode POST qui necessite crsf_token
def reconsiliation_banque(request):
    return render(request, 'page/page_reconsiliation_banque.html')

@login_required(login_url="login/")
@csrf_exempt  # Pour les methode POST qui necessite crsf_token
def reconsiliation_banque_modul(request):
    return render(request, 'page/page_reconsiliation_banque2.html')

@login_required(login_url="login/")
@csrf_exempt  # Pour les methode POST qui necessite crsf_token
def reconsiliation_banque_type_imposition(request):
    return render(request, 'page/page_reconsiliation_banque3.html')

@login_required(login_url="login/")
@csrf_exempt  # Pour les methode POST qui necessite crsf_token
def reconsiliation_banque_all(request):
    return render(request, 'page/page_reconsiliation_banque4.html')

@login_required(login_url="login/")
@csrf_exempt  # Pour les methode POST qui necessite crsf_token
def reconsiliation_banque_paiement(request):
    return render(request, 'page/page_reconsiliation_banque5.html')


