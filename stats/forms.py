from dal import autocomplete

from django import forms
from .models import Hero


class HeroForm(forms.ModelForm):
    name = forms.ModelChoiceField(
    queryset=Hero.objects.all(),
    )

    class Meta:
        model = Hero
        fields = ('__all__')
        widgets = { 'name': autocomplete.ModelSelect2(url='heroes-autocomplete') }
