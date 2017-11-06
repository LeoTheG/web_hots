from django.conf.urls import include, url
from django.contrib import admin
from django.http import HttpResponseRedirect

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^stats/', include('stats.urls', namespace="stats")),
    url(r'^$', lambda r: HttpResponseRedirect('stats/')),
]
