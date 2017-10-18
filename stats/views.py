import json
from django.shortcuts import render
from django.http import HttpResponse
from django.db import models
from .models import Hero
from .models import Enemy
from .tables import HeroTable
from .tables import EnemyTable
from django_tables2 import RequestConfig

with open('stats/stats.json') as json_data:
    d = json.load(json_data)

for h in d:
    newHero = Hero(name=str(h))
    newHero.save()
    for e in d[h]:
        enemy = Enemy(name=str(e), hero=newHero, wins=d[h][e]['wins'], losses=d[h][e]['losses'])
        enemy.save()


def enemies(request, slug):
    hero = Hero.objects.get(slug=slug)
    all_enemies = hero.enemy_set.all()
    table=EnemyTable(all_enemies)
    RequestConfig(request).configure(table)
    #where to declare variables inside view available for html
    return render(request, 'enemies.html', { 'table': table, 'heroName':hero.name} )
def index(request):
    return HttpResponse("This is the stats index.")
def heroes(request):
    table = HeroTable(Hero.objects.all())
    RequestConfig(request).configure(table)
    return render(request, 'heroes.html', { 'table': table})
