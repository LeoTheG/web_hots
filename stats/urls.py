from django.conf.urls import url, include
from . import views
from views import HeroAutoComplete

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^heroes/$', views.heroes, name='heroes'),
    url(r'^heroes/(?P<slug>[-\w]+)/$', views.enemies, name='enemies' ),
    url(r'^maps/(?P<slug>[-\w]+)/$', views.maps, name='maps' ),
    url(r'^heroes-autocomplete/$', HeroAutoComplete.as_view(),
        name='heroes-autocomplete'),
]
