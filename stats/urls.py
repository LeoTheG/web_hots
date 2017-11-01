from django.conf.urls import url, include
from . import views
from views import HeroAutoComplete

urlpatterns = [
    url(r'^$', views.index, name='index'),

    url(r'^maps/$', views.maps, name='maps'),
    url(r'^maps/(?P<slug>[-\w]+)/$', views.map_heroes, name='map_heroes' ),

    url(r'^heroes/$', views.heroes, name='heroes'),
    url(r'^heroes/(?P<slug>[-\w]+)/$', views.hero_main, name='hero_main' ),
    url(r'^heroes/(?P<slug>[-\w]+)/enemies/$', views.enemies, name='enemies' ),
    url(r'^heroes/(?P<slug>[-\w]+)/allies/$', views.allies, name='allies' ),
    url(r'^heroes/(?P<slug>[-\w]+)/maps/$', views.hero_maps, name='hero_maps' ),


    url(r'^heroes-autocomplete/$', HeroAutoComplete.as_view(),
        name='heroes-autocomplete'),
]
