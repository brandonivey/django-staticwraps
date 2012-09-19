""" urls.py """

from django.conf.urls import patterns, include


urlpatterns = patterns('',
    (r'^blogs/content/shared-gen/blogs/', include('staticwraps.urls')),
    )
