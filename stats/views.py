import json
from django.shortcuts import render
from django.http import HttpResponse
from django.db import models
from .models import Hero
from .models import Enemy
from .models import Map
from .models import Ally
from .models import HeroMap
from .models import MapHero
from .models import Talent
from .tables import HeroTable
from .tables import EnemyTable
from .tables import AllyTable
from .tables import MapTable
from .tables import MapHeroTable
from django_tables2 import RequestConfig
import unicodedata
from dal import autocomplete

LEVELS = ['1','4','7','10','13','16','20']
# Instanciate a widget with a bunch of options for select2:
autocomplete.ModelSelect2(
    url='select2_fk',
    attrs={
        # Set some placeholder
        'data-placeholder': 'Autocomplete ...',
        # Only trigger autocompletion after 3 characters have been typed
        'data-minimum-input-length': 1,
    },
)

load_db = 0
# TODO better config file reading
# check to load db

def create_hero(name,total_wins,total_losses):
    newHero = Hero(name=name, total_wins=total_wins,total_losses=total_losses)
    newHero.save()
    return newHero

def normalize(name):
    return unicodedata.normalize('NFD', name).encode('ascii', 'ignore')

with open('stats/config.txt') as f:
    load_db = int(f.readline().rstrip('\n')[len('load_db = ')])

# load the database
if load_db:
    with open('stats/stats.json') as json_data:
        d = json.load(json_data)

    # create maps & map heroes
    for _map in d['maps']:
        new_map = Map(name=_map)
        new_map.save()
        for hero in d['maps'][_map]:
            new_map_hero = MapHero(name=hero,_map=new_map,wins=d['maps'][_map][hero]['wins'], losses=d['maps'][_map][hero]['losses'])
            new_map_hero.save()
    firstHero = True
    for h in d:
        if h == 'maps':
            continue
        normalized_h = normalize(h)
        # runs on first hero creation only
        if (firstHero):
            newHero = create_hero(name=normalized_h, total_wins=d[h]['total_wins'],
                    total_losses=d[h]['total_losses'])
            firstHero = False

        # create new hero only when no other hero exists with same name
        if len(Hero.objects.filter(name=normalized_h)) == 0:
            newHero = create_hero(name=normalized_h, total_wins=d[h]['total_wins'],
                        total_losses=d[h]['total_losses'])
        else:
            newHero = Hero.objects.get(name=normalized_h)

        # create new maps and talents for maps
        for _map in d[h]['maps']:
            normalized_map = normalize(_map)
            newHeroMap = HeroMap(name=normalized_map,wins=d[h]['maps'][_map]['wins'],
                                 losses=d[h]['maps'][_map]['losses'], hero=newHero)
            newHeroMap.save()
            talent_counter = 0
            for talent_level in d[h]['maps'][_map]['talents']:
                #for talent_choice in d[h]['maps'][_map]['talents'][talent][LEVELS[talent_counter]]:
                for talent_choice in d[h]['maps'][_map]['talents'][talent_level]:
                    newTalent = Talent(level=talent_level, name=talent_choice,wins=d[h]['maps'][_map]['talents'][talent_level][talent_choice]['wins'], losses=d[h]['maps'][_map]['talents'][talent_level][talent_choice]['losses'], hero_map=newHeroMap)
                    newTalent.save()
                    talent_counter += 1

        # create new enemies
        for e in d[h]['enemies']:
            normalized_e = normalize(e)

            enemy = Enemy(name=normalized_e, hero=newHero, wins=d[h]['enemies'][e]['wins'],
                          losses=d[h]['enemies'][e]['losses'])
            enemy.save()

        # create new allies
        for ally in d[h]['allies']:
            normalized_name = unicodedata.normalize('NFD', ally).encode('ascii', 'ignore')
            ally = Ally(name=normalized_name, hero=newHero, wins=d[h]['allies'][ally]['wins'],
                        losses=d[h]['allies'][ally]['losses'])
            ally.save()

    with open('stats/config.txt', "w") as r:
        r.write('load_db = 0')

def hero_main(request, slug):
    hero = Hero.objects.get(slug=slug)
    allies_url = 'stats:heroes:'+hero.name+':allies'
    return render(request, 'hero_main.html', {'hero_name':hero.name, 'allies_url': allies_url, 'slug':slug})
def enemies(request, slug):
    hero = Hero.objects.get(slug=slug)
    all_enemies = hero.enemy_set.all()
    enemy_table = EnemyTable(all_enemies)
    RequestConfig(request).configure(enemy_table)
    #where to declare variables inside view available for html
    return render(request, 'enemies.html', { 'enemy_table': enemy_table, 'heroName':hero.name, 'slug':slug} )

def allies(request, slug):
    hero = Hero.objects.get(slug=slug)
    ally_table = AllyTable(hero.ally_set.all())
    RequestConfig(request).configure(ally_table)
    #where to declare variables inside view available for html
    return render(request, 'allies.html', { 'ally_table': ally_table, 'heroName':hero.name, 'slug':slug} )


def map_heroes(request, slug):
    _map = Map.objects.get(slug=slug)
    all_mapheroes = _map.maphero_set.all()
    table = MapHeroTable(all_mapheroes)
    RequestConfig(request).configure(table)
    #where to declare variables inside view available for html
    return render(request, 'map_heroes.html', { 'table': table, 'mapName':_map.name} )

def maps(request):
    table = MapTable(Map.objects.all())
    RequestConfig(request).configure(table)
    return render(request, 'maps.html', { 'table': table})
def index(request):
    return HttpResponse("This is the stats index.")
def heroes(request):
    table = HeroTable(Hero.objects.all())
    RequestConfig(request).configure(table)
    return render(request, 'heroes.html', { 'table': table})

class HeroAutoComplete(autocomplete.Select2QuerySetView):
    template_name = "heroes.html"
    def get_queryset(self):
        print "called get_queryset"
        '''
        # Don't forget to filter out results depending on the visitor !
        if not self.request.user.is_authenticated():
            return Country.objects.none()
        '''

        qs = Hero.objects.all()

        if self.q:
            qs = qs.filter(name__istartswith=self.q)

        return qs

