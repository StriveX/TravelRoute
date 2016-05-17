from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

urlpatterns = [
    # url(r'^login/$', 'django.contrib.auth.views.login'),
    url(r'^register/$', views.register, name='register'),
    url(r'^login/$', views.user_login, name='login'),
    url(r'^logout/$', views.user_logout, name='logout')
]

urlpatterns = format_suffix_patterns(urlpatterns)
