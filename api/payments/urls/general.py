from django.urls import include, path
from rest_framework import routers

from api.payments import views as api

router = routers.DefaultRouter()
router.register("rue-avenue", api.RueOuAvenueViewSet)
router.register("quartier", api.QuartierViewSet)

urlpatterns = [
    path("", include(router.urls)),
    # path("noteimposition/<str:ni_type>/", api.NoteImpositionAPIView.as_view()),
    # path(
    #     "noteimposition/<str:ni_type>/payment/",
    #     api.NoteImpositionPaymentAPIView.as_view(),
    # ),
    path("ping/", api.PingView.as_view()),
    # Contribuable
    # path("contribuable/physique/create/", api.PersonnePhysiqueAPICreateView.as_view()),
]
