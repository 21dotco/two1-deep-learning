"""
    deep21 URL Configuration
"""
from django.conf.urls import url, include
import deep21.views

urlpatterns = [
    url(r'^buy$', deep21.views.buy),
    url(r'^redeem$', deep21.views.redeem),
    url(r'^manifest$', deep21.views.manifest),
    url(r'^payments/', include('two1.bitserv.django.urls')),
]
