from django.conf.urls import url
from django.shortcuts import redirect

from .views import checkattend, detour, success

urlpatterns = [
    url(r'^(?P<class_hash>[a-zA-Z0-9]+)/load/$', detour , name='load'),
    url(r'^check/$', checkattend, name='check'),
    url(r'^success/$', success, name='success'),
]