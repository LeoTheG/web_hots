from dal import autocomplete

from django import forms
from .models import Hero


class HeroForm(forms.ModelForm):
    name = forms.ModelChoiceField(
    queryset=Hero.objects.all(),
    widget=autocomplete.ModelSelect2(url='hero-autocomplete')
    )

    class Meta:
        model = Hero
        fields = ('__all__')

    return render(request, 'stats/heroes.html', {
        'form': form
    })
