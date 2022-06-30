from rest_framework.authtoken import views as token_views
from django.urls import path
from .views import LoginAPIView, UserRetrieveUpdateAPIView

app_name = "authentication"

urlpatterns = [
    path("token/", token_views.obtain_auth_token),
    path("user/", UserRetrieveUpdateAPIView.as_view()),
    path("users/login/", LoginAPIView.as_view()),
]
