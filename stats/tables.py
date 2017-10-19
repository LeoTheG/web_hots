import django_tables2 as tables
from .models import Hero
from .models import Enemy
from django_tables2.utils import A

class HeroTable(tables.Table):
    name = tables.LinkColumn('stats:enemies', args=[A('get_short_name')])
    class Meta:
        model = Hero
        fields = {'name', 'slug'}
        attrs = {'class': 'paleblue', 'td': {'style':'text-align: center;'}}
        exclude = ('slug')
class EnemyTable(tables.Table):
    class Meta:
        model = Enemy
        sequence = ('name', 'win_perc', 'total_games', 'wins', 'losses')
        fields = {'name', 'win_perc', 'total_games','wins','losses' }
        attrs = {'class': 'paleblue', 'td': {'style':'text-align: center;'}}
        exclude= ('wins','losses')
