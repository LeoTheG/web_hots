from django.db import models


class Person(models.Model):
    name = models.CharField(max_length=10)

class Hero(models.Model):
    name = models.CharField(max_length=18)

    '''
    def show_hero_url(self, obj):
        return '<a href="%s">%s</a>' % (obj.hero_url, obj.hero_url)
    show_hero_url.allow_tags = True
    '''

class Enemy(models.Model):
    name = models.CharField(max_length=18)
    hero = models.ForeignKey(Hero, on_delete=models.CASCADE)
    wins = models.IntegerField()
    losses = models.IntegerField()
    def win_perc(self):
        return float(self.wins/self.losses)
    def total_games(self):
        return (self.wins+self.losses)
