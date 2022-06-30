from django.urls import include, path
from rest_framework import routers

from gdaf import api

router = routers.DefaultRouter()
# router.register("rue-avenue", api.RueOuAvenueViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path("etatcivil/document-type-list/", api.DocumentTypeListAPIView.as_view()),
    path(
        "etatcivil/request/avis/<int:reference>/", api.AvisImpositionAPIView.as_view()
    ),
    path("etatcivil/pay/avis/", api.AvisImpositionPayAPIView.as_view()),
]
