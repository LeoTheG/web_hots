import json
from django.shortcuts import render
from django.http import HttpResponse
from django.db import models
from .models import Hero
from .models import Enemy
from .tables import HeroTable
from .tables import EnemyTable
from django_tables2 import RequestConfig
import unicodedata
from dal import autocomplete

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

with open('stats/config.txt') as f:
    load_db = int(f.readline().rstrip('\n')[len('load_db = ')])

# load the database
if load_db:
    with open('stats/stats.json') as json_data:
        d = json.load(json_data)

    firstHero = True
    for h in d:
        normalized_h = unicodedata.normalize('NFD', h).encode('ascii', 'ignore')
        # runs on first hero creation only
        if (firstHero):
            newHero = Hero(name=normalized_h)
            newHero.save()
            firstHero = False

        # create new hero only when no other hero exists with same name
        if len(Hero.objects.filter(name=normalized_h)) == 0:
            newHero = Hero(name=normalized_h)
            newHero.save()

        newHero = Hero.objects.get(name=normalized_h)
        for e in d[h]:
            # create new hero
            normalized_e = unicodedata.normalize('NFD', e).encode('ascii', 'ignore')
            if len(Hero.objects.filter(name=normalized_e)) == 0:
                anotherHero = Hero(name=normalized_e)
                anotherHero.save()
            enemy = Enemy(name=normalized_e, hero=newHero, wins=d[h][e]['wins'], losses=d[h][e]['losses'])
            enemy.save()
    with open('stats/config.txt', "w") as r:
        r.write('load_db = 0')

def enemies(request, slug):
    hero = Hero.objects.get(slug=slug)
    all_enemies = hero.enemy_set.all()
    table = EnemyTable(all_enemies)
    RequestConfig(request).configure(table)
    #where to declare variables inside view available for html
    return render(request, 'enemies.html', { 'table': table, 'heroName':hero.name} )
def index(request):
    return HttpResponse("This is the stats index.")
def heroes(request):
    table = HeroTable(Hero.objects.all())
    RequestConfig(request).configure(table)
    return render(request, 'heroes.html', { 'table': table})

class HeroAutoComplete(autocomplete.Select2QuerySetView):
    template_name = "heroes.html"
    print "in HeroAutoComplete"
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

