from django.conf.urls import patterns, url


urlpatterns = patterns(
    'wtl.wtlib.views',
    url(r'^$', 'home', name='home'),
)
