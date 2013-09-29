from django.conf.urls import patterns, include, url
from django.contrib import admin


admin.autodiscover()

urlpatterns = patterns(
    '',
    url(r'^admin_tools/', include('admin_tools.urls')),
    url(r'^', include('wtl.wtlib.urls')),
    url(r'^slr/', include('wtl.streaming_log_response.urls')),
    url(r'^admin/wtgithub/', include('wtl.wtgithub.admin.urls')),
    url(r'^admin/', include(admin.site.urls)),
)
