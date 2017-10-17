from django.shortcuts import render
from django.http import HttpResponse
from django.db import models
from stats.models import Person

def index(request):
    return HttpResponse("This is the stats index.")
def people(request):
    return render(request, 'people.html', {'people': Person.objects.all()})

