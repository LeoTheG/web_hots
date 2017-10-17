# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

class Person(models.Model):
    name = models.CharField(verbose_name="full name",max_length=10)

# Create your models here.
