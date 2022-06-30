# from .enrollement import urlpatterns as erl_urlpatterns
from .payments import urlpatterns as pay_urlpatterns
from .general import urlpatterns as gn_urlpatterns

# from .etat_civil import urlpatterns as et_urlpatterns


# urlpatterns = erl_urlpatterns + pay_urlpatterns + gn_urlpatterns  # + et_urlpatterns
urlpatterns = pay_urlpatterns + gn_urlpatterns  # + et_urlpatterns
