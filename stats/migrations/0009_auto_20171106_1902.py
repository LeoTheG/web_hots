# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-11-06 19:02
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('stats', '0008_auto_20171104_2214'),
    ]

    operations = [
        migrations.CreateModel(
            name='HeroMapTalent',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('level', models.IntegerField()),
                ('name', models.CharField(max_length=64)),
                ('wins', models.IntegerField()),
                ('losses', models.IntegerField()),
                ('hero_map', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='stats.HeroMap')),
            ],
        ),
        migrations.RemoveField(
            model_name='talent',
            name='hero_map',
        ),
        migrations.AddField(
            model_name='talent',
            name='cooldown',
            field=models.IntegerField(default=-1),
        ),
        migrations.AddField(
            model_name='talent',
            name='description',
            field=models.CharField(default=b'', max_length=1024),
        ),
        migrations.AddField(
            model_name='talent',
            name='heroName',
            field=models.CharField(default=b'', max_length=32),
        ),
        migrations.AddField(
            model_name='talent',
            name='url',
            field=models.CharField(default=b'', max_length=128),
        ),
    ]
