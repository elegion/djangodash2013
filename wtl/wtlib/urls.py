from django.conf.urls import patterns, url


urlpatterns = patterns(
    'wtl.wtlib.views',

    url(r'^$', 'home', name='home'),

    url(r'^libraries/$', 'libraries_list',
        {'language_slug': None},
        name='wtlib_libraries_list'),
    url(r'^libraries/(?P<language_slug>[\w\d-]+)/$', 'libraries_list',
        name='wtlib_libraries_list'),
    url(r'^libraries/(?P<language_slug>[\w\d-]+)/(?P<library_slug>[\w\d-]+)$',
        'library', name='wtlib_library'),

    url(r'^projects/$', 'projects_list', name='wtlib_projects_list'),
    url(r'^projects/(?P<project_slug>[\w\d-]+)$', 'project',
        name='wtlib_project'),
)
