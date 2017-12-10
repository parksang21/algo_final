from django.conf.urls import url
from django.shortcuts import redirect

from .views import today_class, class_detail, date_detail, refresh, teamBuild, date_option

urlpatterns = [
    url(r'^(?P<id>\d+)/$', today_class, name="class_list"),
    url(r'^detail/(?P<id>\d+)/$', class_detail, name="class_detail"),
    url(r'^detail/(?P<c_id>\d+)/(?P<id>\d+)/option/$', date_option ,name="date_option"),
    

    url(r'^date/(?P<c_id>\d+)/(?P<id>\d+)/detail/$', date_detail, name="date_detail"),
    url(r'^date/(?P<c_id>\d+)/(?P<id>\d+)/team/$', teamBuild, name="team"),

    url(r'^refresh/$', refresh, name="refresh"),
]