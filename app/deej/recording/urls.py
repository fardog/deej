from django.conf.urls import patterns, url


urlpatterns = patterns('deej.recording',
    url(r'^$', 'views.index'),
)
