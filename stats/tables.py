import django_tables2 as tables
from .models import Person
from .models import Hero

class HeroTable(tables.Table):
    class Meta:
        model = Hero
        # add class="paleblue" to <table> tag
        attrs = {'class': 'paleblue'}
