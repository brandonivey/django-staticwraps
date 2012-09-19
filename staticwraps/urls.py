"""
staticwraps.urls
"""

from django.conf.urls.defaults import patterns, url


urlpatterns = patterns('staticwraps.views', )
urlpatterns += patterns('',
    url(r'^(?P<url_path>.*\/.+?.xml)/$', 'staticwraps.views.render_simple_content', name='simplewrap-render'),
    url(r'^(?P<url_path>.*)/$', 'staticwraps.views.render_content', name='staticwrap-render'),
    )
