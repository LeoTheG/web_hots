from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^heroes/$', views.heroes, name='heroes'),
    url(r'^heroes/(?P<hero_id>[0-9]+)/$', views.enemies, name='enemies')
]
