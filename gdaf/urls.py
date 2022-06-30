"""gdaf URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include, handler404, handler500
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.conf import settings
from django.contrib import admin
from django.contrib.auth import views
from gdaf.views import (
    home,
    error_404,
    error_500,
    dashboard_contribuable,
    dashboard_communication,
    dashboard_imposition,
    dashboard_recette,
    dashboard_technique,
    dashboard_transport,
)
from .forms import LoginForm
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

admin.site.site_header = settings.ADMIN_SITE_HEADER
admin.site.site_title = settings.ADMIN_SITE_TITLE

urlpatterns = [
    url(r"^$", home, name="home"),
    # Tableaux de bord selon menu
    url(
        r"^dashboard/contribuable/$",
        dashboard_contribuable,
        name="dashboard_contribuable",
    ),
    url(
        r"^dashboard/communication/$",
        dashboard_communication,
        name="dashboard_communication",
    ),
    url(r"^dashboard/imposition/$", dashboard_imposition, name="dashboard_imposition"),
    url(r"^dashboard/recette/$", dashboard_recette, name="dashboard_recette"),
    url(r"^dashboard/technique/$", dashboard_technique, name="dashboard_technique"),
    url(r"^dashboard/transport/$", dashboard_transport, name="dashboard_transport"),
    url(
        r"^accounts/profile/", home, name="home"
    ),  # à verifier erreur django admin redirection
    url(r"^admin/", admin.site.urls),
    url(
        r"^admin/", lambda _: redirect("admin:index"), name="index_admin"
    ),  # resoudre l'erreur pour passer en admin
    url(r"", include("mod_parametrage.urls")),
    url(r"", include("mod_crm.urls")),
    url(r"", include("mod_transport.urls")),
    url(r"", include("mod_activite.urls")),
    url(r"", include("mod_finance.urls")),
    url(r"", include("mod_foncier.urls")),
    url(r"", include("mod_reporting.urls")),
    url(r"", include("mod_documents.urls")),
    url(r"", include("mod_helpers.urls")),
    # Added api urls
    url(r"", include("api.urls")),
    url(
        r"^login/$",
        views.LoginView.as_view(
            template_name="login.html", authentication_form=LoginForm
        ),
        name="login",
    ),
    url(
        r"^logout/$",
        views.LogoutView.as_view(template_name="registration/logout.html"),
        name="logout",
    ),
    # url(r'^logout/$', views.LogoutView.as_view(), {'next_page': 'login.html'}),
    url(r"^error-404$", error_404, name="error_404"),
    url(r"^error-500$", error_500, name="error_500"),
]

urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


# handler404 = error_404
# handler500 = error_500
# Reading an excel file using Python
# import xlrd
#
# # Give the location of the file
# loc = (settings.MEDIA_URL+'fichier_rapport_bank/7d2ed4f0983e4bdbb4be97107bbe3b47.xlsx')
#
# # To open Workbook
# wb = xlrd.open_workbook(loc)
# sheet = wb.sheet_by_index(0)
#
# # For row 0 and column 0
# print(sheet.cell_value(0, 0))