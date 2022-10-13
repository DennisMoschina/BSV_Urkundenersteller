from django.template.defaulttags import url
from django.urls import path

from . import views


urlpatterns = [
    path('', views.index, name='index'),
    # url(r'^upload/$', views.upload_file_from, name='upload'),
    path('upload/', views.upload_winner_csv, name='upload_winner_csv'),
]