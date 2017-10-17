from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^people/$', views.people, name='people'),
    url(r'^heroes/$', views.heroes, name='heroes'),
]
