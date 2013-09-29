from django.conf.urls import patterns, url


urlpatterns = patterns(
    'wtl.wtlib.views',
    url(r'^$', 'home', name='home'),
    url(r'^projects/(?P<project_id>\d+)$', 'project', name='wtlib_project'),
)
