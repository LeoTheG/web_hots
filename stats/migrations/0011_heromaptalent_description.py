# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-11-06 20:44
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stats', '0010_auto_20171106_1953'),
    ]

    operations = [
        migrations.AddField(
            model_name='heromaptalent',
            name='description',
            field=models.CharField(default=b'', max_length=1024),
        ),
    ]
