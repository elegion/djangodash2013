from django.conf.urls import patterns, url


urlpatterns = patterns(
    'wtl.wtgithub.admin.views',

    url(r'^crawl/$', 'crawl', name='wtgithub_admin_crawl'),
)
