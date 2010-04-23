from django.conf.urls.defaults import *

urlpatterns = patterns('timeline.views',
     url(r'^$', 'rss', name='rss_latest'),
     url(r'^etiket/(?P<tag_slug>[-\w]+)/$', 'rss', name='rss_tag'),
     url(r'^(?P<model_name>\w+)/$', 'rss', name='rss_model'),
     url(r'^(?P<model_name>\w+)/(?P<tag_slug>[\w]+)/$', 'rss', name='rss_tag_model'),
)
