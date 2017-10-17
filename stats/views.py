import json
from django.shortcuts import render
from django.http import HttpResponse
from django.db import models
from stats.models import Person
from .models import Hero
from .tables import HeroTable
from django_tables2 import RequestConfig

with open('stats/stats.json') as json_data:
    d = json.load(json_data)
    print "type of d is " + str(d.__class__)

dicNames = {}
for h in d:
    print str(h)
    #hero = Hero.objects.create(name=str(h))
    hero = Hero(name=str(h))
    print "Length of hero objects=" +str(Hero.objects.count)
    hero.save()
    print "\tNo errors after save"

def index(request):
    return HttpResponse("This is the stats index.")
def people(request):
    return render(request, 'people.html', {'people': Person.objects.all()})
def heroes(request):
    #table = HeroTable(d)
    print "Length of hero objects=" +str(Hero.objects.count)
    table = HeroTable(Hero.objects.all())
    RequestConfig(request).configure(table)
    return render(request, 'heroes.html', { 'table': table})

