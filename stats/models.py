from django.db import models

class Person(models.Model):
    name = models.CharField(max_length=10)

class Hero(models.Model):
    print "Created Hero"
    name = models.CharField(max_length=18)

