import django_tables2 as tables
from .models import Hero
from .models import Enemy
from .models import Ally
from .models import Map
from .models import MapHero
from .models import HeroMap
from .models import Talent
from .models import HeroMapTalent

from django_tables2.utils import A
from django.db.models import F

class TotalGamesColumn(tables.Column):
    def render(self, record):
        return str(record.wins + record.losses)
    def order(self, queryset, is_descending):
        queryset = queryset.annotate(amount=F('wins')+F('losses')).order_by(('-' if is_descending else '') + 'amount')
        return (queryset, True)

class WinPercColumn(tables.Column):
    def render(self, record):
        return str(int((record.wins / ((record.wins+record.losses)*1.0) * 100))) + '%'
    def order(self, queryset, is_descending):
        queryset = queryset.annotate(win_perc=(F('wins')/((F('losses')+F('wins'))*1.0))).order_by(('-' if is_descending else '') + 'win_perc')
        return (queryset, True)

# table for heroes
class HeroTable(tables.Table):
    name = tables.LinkColumn('stats:hero_main', args=[A('get_short_name')])
    win_perc = WinPercColumn(empty_values=())
    class Meta:
        model = Hero
        fields = {'name','win_perc', 'slug'}
        sequence = ('name', 'win_perc')
        exclude = ('slug')
        attrs = {}

# table for maps
class MapTable(tables.Table):
    name = tables.LinkColumn('stats:map_heroes', args=[A('get_short_name')])
    class Meta:
        model = Map
        fields = {'name', 'slug'}
        exclude = ('slug')
        attrs = {}
# enemies of heroes
class EnemyTable(tables.Table):
    name = tables.LinkColumn('stats:hero_main', args=[A('get_short_name')])
    win_perc = WinPercColumn(empty_values=())
    total_games = TotalGamesColumn(empty_values=())

    class Meta:
        model = Enemy
        sequence = ('name', 'win_perc', 'total_games', 'wins', 'losses')
        fields = {'name', 'win_perc', 'total_games','wins','losses' }
        attrs = {}
        #        }
        exclude= ('wins','losses')
# allies of heroes
class AllyTable(tables.Table):
    name = tables.LinkColumn('stats:hero_main', args=[A('get_short_name')])
    win_perc = WinPercColumn(empty_values=())
    total_games = TotalGamesColumn(empty_values=())

    class Meta:
        model = Ally
        sequence = ('name', 'win_perc', 'total_games', 'wins', 'losses')
        fields = {'name', 'win_perc', 'total_games','wins','losses' }
        attrs = {}
        #        }
        exclude= ('wins','losses')
# heroes of map
class MapHeroTable(tables.Table):
    name = tables.LinkColumn('stats:hero_main',
            args=[A('get_short_name')])
    win_perc = WinPercColumn(empty_values=())
    total_games = TotalGamesColumn(empty_values=())

    class Meta:
        model = MapHero
        sequence = ('name', 'win_perc', 'total_games', 'wins', 'losses')
        fields = {'name', 'win_perc', 'total_games','wins','losses' }
        attrs = {}
        exclude= ('wins','losses')

# maps of heroes
class HeroMapTable(tables.Table):
    name = tables.LinkColumn('stats:hero_map_talents',
            args=[A('hero.get_short_name'),A('get_short_name')])
    win_perc = WinPercColumn(empty_values=())
    total_games = TotalGamesColumn(empty_values=())

    class Meta:
        model = HeroMap
        sequence = ('name', 'win_perc', 'total_games', 'wins', 'losses')
        fields = {'name', 'win_perc', 'total_games','wins','losses' }
        attrs = {}
        exclude= ('wins','losses')


class DescriptionColumn(tables.Column):
    def render(self,record):
        return record.description

class HeroMapTalentTable(tables.Table):
    win_perc = WinPercColumn(empty_values=())
    total_games = TotalGamesColumn(empty_values=())
    description = DescriptionColumn(attrs={'td':{'id':'description'}},orderable=False)
    class Meta:
        model = HeroMapTalent
        sequence = ('level','name','win_perc','description', 'total_games','wins','losses')
        exclude = ('wins','losses','hero_map','id')

class HeroTalentTable(tables.Table):
    win_perc = WinPercColumn(empty_values=())
    total_games = TotalGamesColumn(empty_values=())
    description = DescriptionColumn(attrs={'td':{'id':'description'}},orderable=False)
    class Meta:
        model = Talent
        sequence = ('level','name','win_perc','description', 'total_games','wins','losses')
        exclude = ('wins','losses','url','id','cooldown','heroName')
