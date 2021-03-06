import json
from django.shortcuts import render
from django.http import HttpResponse
from django.db import models
from .models import Hero
from .models import Enemy
from .models import Map
from .models import Ally
from .models import HeroMapTalent
from .models import HeroMap
from .models import MapHero
from .models import Talent
from .tables import HeroTable
from .tables import EnemyTable
from .tables import AllyTable
from .tables import MapTable
from .tables import MapHeroTable
from .tables import HeroMapTable
from .tables import HeroTalentTable
from .tables import HeroMapTalentTable
from django_tables2 import RequestConfig
import unicodedata
from dal import autocomplete

LEVELS = ['1','4','7','10','13','16','20']

load_db = 0
# TODO better config file reading
# check to load db

def create_hero(name,wins,losses):
    newHero = Hero(name=name, wins=wins,losses=losses)
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

    # create talents
    for t in d['talents']:
        if (('description' in d['talents'][t])==False) or (('short_name' in d['talents'][t])==False) or (('level' in d['talents'][t])==False) or (('url' in d['talents'][t])==False):
            continue
        for hero in d['talents'][t]['heroes']:
            '''
            if ('url' in d['talents'][t]) == False:
                if (d['talents'][t]['level']==None):
                    talent = Talent(name=d['talents'][t]['short_name'],level=-1, wins=d['talents'][t]['heroes'][hero]['wins'],losses=d['talents'][t]['heroes'][hero]['losses'],description=d['talents'][t]['description'], url='', cooldown=d['talents'][t]['cooldown'],heroName=hero)
                else:
                    talent = Talent(name=d['talents'][t]['short_name'],level=d['talents'][t]['level'], wins=d['talents'][t]['heroes'][hero]['wins'],losses=d['talents'][t]['heroes'][hero]['losses'],description=d['talents'][t]['description'], url='', cooldown=d['talents'][t]['cooldown'],heroName=hero)

                talent = Talent(name=d['talents'][t]['short_name'],level=d['talents'][t]['level'], wins=d['talents'][t]['heroes'][hero]['wins'],losses=d['talents'][t]['heroes'][hero]['losses'],description=d['talents'][t]['description'], url='', cooldown=d['talents'][t]['cooldown'],heroName=hero)
            else:
                if (d['talents'][t]['level']==None):
                    talent = Talent(name=d['talents'][t]['short_name'],level=-1, wins=d['talents'][t]['heroes'][hero]['wins'],losses=d['talents'][t]['heroes'][hero]['losses'],description=d['talents'][t]['description'], url=d['talents'][t]['url'], cooldown=d['talents'][t]['cooldown'],heroName=hero)
                else:
                    talent = Talent(name=d['talents'][t]['short_name'],level=d['talents'][t]['level'], wins=d['talents'][t]['heroes'][hero]['wins'],losses=d['talents'][t]['heroes'][hero]['losses'],description=d['talents'][t]['description'], url=d['talents'][t]['url'], cooldown=d['talents'][t]['cooldown'],heroName=hero)
            '''
            talent = Talent(name=d['talents'][t]['short_name'],level=d['talents'][t]['level'], wins=d['talents'][t]['heroes'][hero]['wins'],losses=d['talents'][t]['heroes'][hero]['losses'],description=d['talents'][t]['description'], url=d['talents'][t]['url'], cooldown=d['talents'][t]['cooldown'],heroName=hero)
            talent.save()

    firstHero = True
    for h in d:
        if h == 'maps' or h == 'talents':
            continue
        normalized_h = normalize(h)
        # runs on first hero creation only
        if (firstHero):
            newHero = create_hero(name=normalized_h, wins=d[h]['total_wins'],
                    losses=d[h]['total_losses'])
            firstHero = False

        # create new hero only when no other hero exists with same name
        if len(Hero.objects.filter(name=normalized_h)) == 0:
            newHero = create_hero(name=normalized_h, wins=d[h]['total_wins'],
                        losses=d[h]['total_losses'])
        else:
            newHero = Hero.objects.get(name=normalized_h)

        # create new maps and talents for maps
        for _map in d[h]['maps']:
            normalized_map = normalize(_map)
            newHeroMap = HeroMap(name=normalized_map,wins=d[h]['maps'][_map]['wins'], losses=d[h]['maps'][_map]['losses'], hero=newHero)
            newHeroMap.save()
            talent_counter = 0
            for talent_level in d[h]['maps'][_map]['talents']:
                for talent_choice in d[h]['maps'][_map]['talents'][talent_level]:
                    if len(Talent.objects.filter(name=talent_choice)) == 0:
                        continue
                    newHeroMapTalent = HeroMapTalent(level=talent_level, name=talent_choice,wins=d[h]['maps'][_map]['talents'][talent_level][talent_choice]['wins'], losses=d[h]['maps'][_map]['talents'][talent_level][talent_choice]['losses'], hero_map=newHeroMap,description=Talent.objects.filter(name=talent_choice)[0].description)
                    newHeroMapTalent.save()
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
    wins = hero.wins
    losses = hero.losses
    win_perc = int((wins / ((wins+losses)*1.0) * 100))
    hero_maps = hero.heromap_set.all()

    best_map_dict = {'0':{'name':'','win_perc':0},
                    '1':{'name':'','win_perc':0},
                    '2':{'name':'','win_perc':0},
                    '3':{'name':'','win_perc':0},
                    '4':{'name':'','win_perc':0},
                    }

    best_maps = [0]*5
    best_map_names = ['']*5
    for _map in hero_maps:
        map_win_perc = int((_map.wins / ((_map.wins+_map.losses)*1.0) * 100))
        # calculate the top 5 maps
        for i in range(0,5):
            if map_win_perc > best_maps[i]:
                j = 4
                while j > i:
                    best_map_dict[str(j)]['win_perc'] = best_map_dict[str(j-1)]['win_perc']
                    best_map_dict[str(j)]['name'] = best_map_dict[str(j-1)]['name']
                    j -= 1
                best_maps[i]=map_win_perc
                best_map_names[i]=_map.name
                break


    return render(request, 'hero_main.html', {'hero_name':hero.name,'slug':slug, 'win_perc':win_perc, 'hero':hero, 'bestMapNames':best_map_names, 'bestMapWinPercs':best_maps})

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

def hero_maps(request, slug):
    hero = Hero.objects.get(slug=slug)
    hero_map_table = HeroMapTable(hero.heromap_set.all())
    RequestConfig(request).configure(hero_map_table)
    #where to declare variables inside view available for html
    return render(request, 'hero_maps.html', { 'table': hero_map_table, 'heroName':hero.name, 'slug':slug} )

def hero_map_talents(request, heroslug,mapslug):
    hero = Hero.objects.get(slug=heroslug)
    hero_map = HeroMap.objects.get(slug=mapslug,hero=hero)
    all_map_talents = hero_map.heromaptalent_set.all()
    table = HeroMapTalentTable(all_map_talents)
    RequestConfig(request).configure(table)
    return render(request, 'hero_map_talents.html', {'table': table, 'mapName':hero_map.name,'mapslug':mapslug,'heroslug':heroslug,'heroName':hero.name} )

def hero_talents(request, heroslug):
    hero = Hero.objects.get(slug=heroslug)
    all_talents = Talent.objects.filter(heroName=hero.name)
    table = HeroTalentTable(all_talents)
    RequestConfig(request).configure(table)
    return render(request, 'hero_talents.html', {'table': table,'heroslug':heroslug,'heroName':hero.name} )


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
    return render(request, 'index.html')
    #return HttpResponse("This is the stats index.")
def heroes(request):
    table = HeroTable(Hero.objects.all())
    RequestConfig(request).configure(table)
    return render(request, 'heroes.html', { 'table': table})
