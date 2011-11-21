from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('subscriptions.views',
    url(r'^$', 'subscribe', name='subscribe'),
    url(r'^(\d+)/sucesso/$', 'success', name='success'),
)