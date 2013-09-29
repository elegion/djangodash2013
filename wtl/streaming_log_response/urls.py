from django.conf.urls import patterns, url


urlpatterns = patterns(
    'wtl.streaming_log_response.views',

    url(r'^$', 'test', name='streamin_log_response_test'),
    url(r'^2$', 'test2', name='streamin_log_response_test'),
)
