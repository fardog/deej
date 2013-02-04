from django.conf.urls import patterns, include, url
from django.contrib.auth.views import logout_then_login

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

from dajaxice.core import dajaxice_autodiscover, dajaxice_config
dajaxice_autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'deej.views.home', name='home'),
    url(r'^recording/', include('deej.recording.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(dajaxice_config.dajaxice_url, include('dajaxice.urls')),

    url(r'^login/$', 'deej.views.login'),
    url(r'^logout/$', logout_then_login),
    url(r'^register/$', 'deej.views.register'),
    url(r'^$', 'deej.views.index'),
)
