import django_tables2 as tables
from .models import Hero
from .models import Enemy

class HeroTable(tables.Table):
    #edit_entries = tables.TemplateColumn('<a href="{% url \'enemies\' record.id %}">Edit</a>')
    class Meta:
        model = Hero
        fields = {'name'}
        attrs = {'class': 'paleblue', 'td': {'style':'text-align: center;'}}
class EnemyTable(tables.Table):
    class Meta:
        model = Enemy
        sequence = ('name', 'win_perc', 'total_games', 'wins', 'losses')
        fields = {'name', 'win_perc', 'total_games','wins','losses' }
        attrs = {'class': 'paleblue', 'td': {'style':'text-align: center;'}}

