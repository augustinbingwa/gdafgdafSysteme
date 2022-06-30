from django.urls import path
from .views import *

urlpatterns = [
    path('check_amount_nic/', amountToPaybyNic.as_view(), name='getContribuableByNIC'),
    path('check_all_amount_nic/', allAmountToPaybyNic.as_view(), name='allAmountToPaybyNic'),
    path('check_amount_byIdCard/', amountToPaybyIdCard.as_view(), name='amountToPaybyIdCard'),
    path('check_all_amount_byIdCard/', allAmountToPaybyIdCard.as_view(), name='allAmountToPaybyIdCard'),
]