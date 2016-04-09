from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

urlpatterns = [
    url(r'^$', views.map, name='index'),
    url(r'^load_places/$', views.load_places, name='create_location'),
    url(r'^create_place/$', views.create_place, name='create_location'),
    url(r'^(?P<location_id>)[0-9]+/$', views.location, name='location_detail'),
    url(r'^load_route/$', views.load_route, name='create_location'),
    url(r'^create_route/$', views.create_route, name='create_location'),
    # url(r'^(?P<location_id>)[0-9]+/$', views.location, name='location_detail'),
    url(r'^api/$', views.LocationList.as_view()),
    url(r'^api/(?P<pk>[0-9]+)/$', views.LocationDetail.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
