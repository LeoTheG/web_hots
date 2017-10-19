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

firstHero = True
for h in d:
    # runs on first hero creation only
    if (firstHero):
        newHero = Hero(name=str(h))
        newHero.save()
        print "Created first hero: ", str(h)
        firstHero = False

    #newHero = Hero.objects.all()[0]

    # create new hero only when no other hero exists with same name
    if len(Hero.objects.filter(name=str(h))) == 0:
        newHero = Hero(name=str(h))
        newHero.save()

    newHero = Hero.objects.get(name=str(h))
    #print "Created hero with name", str(h)
    for e in d[h]:
        # create new hero
        if len(Hero.objects.filter(name=str(e))) == 0:
            #print "\tNo heroes with name", str(e)
            anotherHero = Hero(name=str(e))
            anotherHero.save()
            #enemy = Enemy(name=str(e), hero=anotherHero, wins=d[h][e]['wins'], losses=d[h][e]['losses'])
            #enemy.save()
        enemy = Enemy(name=str(e), hero=newHero, wins=d[h][e]['wins'], losses=d[h][e]['losses'])
        enemy.save()


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
