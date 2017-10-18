from django.db import models
from slugify import slugify

class Hero(models.Model):
    name = models.CharField(max_length=18)
    slug = models.SlugField(unique=True)

    def get_slug(self):
        print "called get_slug()"
        return slugify(self.name)
    def save(self, *args, **kwargs):
        print "saving hero"
        if not self.slug:
            self.slug = self.get_slug()
        print "saving hero super()"
        super(Hero,self).save()


class Enemy(models.Model):
    name = models.CharField(max_length=18)
    hero = models.ForeignKey(Hero, on_delete=models.CASCADE)
    wins = models.IntegerField()
    losses = models.IntegerField()
    def win_perc(self):
        if (self.losses == 0) return 100
        return float(self.wins/self.losses)*100
    def total_games(self):
        return (self.wins+self.losses)
