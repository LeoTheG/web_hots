from django.db import models
from slugify import slugify
import re, string


class Hero(models.Model):
    name = models.CharField(max_length=18)
    slug = models.SlugField(unique=True)
    wins = models.IntegerField(default=0)
    losses = models.IntegerField(default=0)

    def get_slug(self):
        #return slugify(self.name)
        return slugify(self.get_short_name())
    def get_short_name(self):
        return slugify(re.sub(r'\W+', '', self.name))
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self.get_slug()
        super(Hero,self).save(*args, **kwargs)

    def get_win_perc(self):
        return int((self.wins / ((self.losses+self.losses)*1.0) * 100))
    def get_maps(self):
#        return self.heromap_set.all().order_by('get_win_perc')[:5]
        return self.heromap_set.all()
        #return HeroMap.objects.filter(hero=self).order_by('-win_perc')[:5]


class Enemy(models.Model):
    name = models.CharField(max_length=18)
    hero = models.ForeignKey(Hero, on_delete=models.CASCADE)
    wins = models.IntegerField()
    losses = models.IntegerField()

    def get_short_name(self):
        return slugify(re.sub(r'\W+', '', self.name))



class Map(models.Model):
    name = models.CharField(max_length=32)
    slug = models.SlugField(unique=True)

    def get_slug(self):
        return slugify(self.get_short_name())
    def get_short_name(self):
        return slugify(re.sub(r'\W+', '', self.name))
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self.get_slug()
        super(Map,self).save()

class MapHero(models.Model):
    name = models.CharField(max_length=32)
    _map = models.ForeignKey(Map, on_delete=models.CASCADE)
    wins = models.IntegerField()
    losses = models.IntegerField()

    def get_short_name(self):
        return slugify(re.sub(r'\W+', '', self.name))

class Ally(models.Model):
    name = models.CharField(max_length=18)
    hero = models.ForeignKey(Hero, on_delete=models.CASCADE)
    wins = models.IntegerField()
    losses = models.IntegerField()

    def get_short_name(self):
        return slugify(re.sub(r'\W+', '', self.name))

class HeroMap(models.Model):
    name = models.CharField(max_length=32)
    wins = models.IntegerField()
    losses = models.IntegerField()
    hero = models.ForeignKey(Hero, on_delete=models.CASCADE)
    slug = models.SlugField()

    def get_slug(self):
        '''
        print "get_slug for heroMap: " +self.name + " = " + slugify(self.hero.get_short_name()+self.get_short_name())
        return slugify(self.hero.get_short_name()+self.get_short_name())
    '''
        return slugify(self.get_short_name())

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self.get_slug()
        super(HeroMap,self).save(*args, **kwargs)


    def get_short_name(self):
        return slugify(re.sub(r'\W+', '', self.name))

class Talent(models.Model):
    name = models.CharField(max_length=64)
    level = models.IntegerField()
    wins = models.IntegerField()
    losses = models.IntegerField()
    description = models.CharField(default='',max_length=1024)
    url = models.CharField(default='',max_length=128)
    cooldown = models.IntegerField(default=-1,null=True)
    heroName = models.CharField(default='',max_length=32)

class HeroMapTalent(models.Model):
    level = models.IntegerField()
    name = models.CharField(max_length=64)
    wins = models.IntegerField()
    losses = models.IntegerField()
    hero_map = models.ForeignKey(HeroMap, on_delete=models.CASCADE)
    description = models.CharField(default='',max_length=1024)

    '''
    def get_description(self):
        talent = Talent.objects.get(name=self.name)
        return talent.description
    '''
