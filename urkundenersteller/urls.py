from django.template.defaulttags import url
from django.urls import path

from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('urkunden', views.previously_created_certificates, name='urkunden')
]