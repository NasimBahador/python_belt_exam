from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^destination/(?P<id>\d+)$', views.destination, name='destination'),
    url(r'^add_trip$', views.add_trip, name='add_trip'),
    url(r'^create$', views.create, name='create'),
    url(r'^join/(?P<id>\d+)$', views.join, name='join'),
    url(r'^logout$', views.logout, name='logout'),

]
