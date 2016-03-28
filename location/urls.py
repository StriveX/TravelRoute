from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

urlpatterns = [
    url(r'^(?P<location_id>)/$', views.location, name='index'),
    url(r'^api/$', views.LocationList.as_view()),
    url(r'^api/(?P<pk>[0-9]+)/$', views.LocationDetail.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)