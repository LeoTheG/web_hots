import django_tables2 as tables
from .models import Hero
from .models import Enemy
from django_tables2.utils import A
from django.db.models import F

class HeroTable(tables.Table):
    name = tables.LinkColumn('stats:enemies', args=[A('get_short_name')])
    class Meta:
        model = Hero
        fields = {'name', 'slug'}
        attrs = {'class': 'paleblue', 'td': {'style':'text-align: center;'}}
        exclude = ('slug')

class TotalGamesColumn(tables.Column):
    def render(self, record):
        #print "rendering enemy: " + str(record.name) + ", with " + str(record.wins) + " wins and " + str(record.losses) + " losses"
        return str(record.wins + record.losses)
    def order(self, queryset, is_descending):
        queryset = queryset.annotate(amount=F('wins')+F('losses')).order_by(('-' if is_descending else '') + 'amount')
        return (queryset, True)

class WinPercColumn(tables.Column):
    def render(self, record):
        #return str("{0:.2f}".format((record.wins / ((record.wins+record.losses)*1.0) * 100)))
        return str(int((record.wins / ((record.wins+record.losses)*1.0) * 100))) + '%'
    def order(self, queryset, is_descending):
        queryset = queryset.annotate(win_perc=(F('wins')/((F('losses')+F('wins'))*1.0))).order_by(('-' if is_descending else '') + 'win_perc')
        return (queryset, True)

class EnemyTable(tables.Table):
    name = tables.LinkColumn('stats:enemies', args=[A('get_short_name')])
    win_perc = WinPercColumn(empty_values=())
    total_games = TotalGamesColumn(empty_values=())

    class Meta:
        model = Enemy
        sequence = ('name', 'win_perc', 'total_games', 'wins', 'losses')
        fields = {'name', 'win_perc', 'total_games','wins','losses' }
        attrs = {'class': 'paleblue', 'td': {'style':'text-align: center;'}}
        exclude= ('wins','losses')
