from django.db import models
from slugify import slugify
import re, string

class Hero(models.Model):
    name = models.CharField(max_length=18)
    slug = models.SlugField(unique=True)
    total_wins = models.IntegerField(default=0)
    total_losses = models.IntegerField(default=0)

    def get_slug(self):
        #return slugify(self.name)
        return slugify(self.get_short_name())
    def get_short_name(self):
        return slugify(re.sub(r'\W+', '', self.name))
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self.get_slug()
        print "Saving hero " + self.name
        super(Hero,self).save(*args, **kwargs)


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

class Talent(models.Model):
    level = models.IntegerField()
    name = models.CharField(max_length=64)
    wins = models.IntegerField()
    losses = models.IntegerField()
    hero_map = models.ForeignKey(HeroMap, on_delete=models.CASCADE)
