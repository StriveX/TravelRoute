from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

urlpatterns = [
    url(r'^login/$', 'django.contrib.auth.views.login'),
]

urlpatterns = format_suffix_patterns(urlpatterns)
