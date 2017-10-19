from django.db import models
from slugify import slugify
import re, string

class Hero(models.Model):
    name = models.CharField(max_length=18)
    slug = models.SlugField(unique=True)

    def get_slug(self):
        return slugify(self.name)
    def get_short_name(self):
        return slugify(re.sub(r'\W+', '', self.name))
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self.get_slug()
        super(Hero,self).save()


class Enemy(models.Model):
    name = models.CharField(max_length=18)
    hero = models.ForeignKey(Hero, on_delete=models.CASCADE)
    wins = models.IntegerField()
    losses = models.IntegerField()
    def win_perc(self):
        if (self.losses == 0): return 100
        return float(self.wins/self.losses)*100
    def total_games(self):
        return (self.wins+self.losses)
