""" staticwraps.models
    models to support wrapping static content and map to categories
"""

from django.conf import settings
from django.contrib.sites.models import Site
from django.db import models

import jsonfield


class StaticWrap(models.Model):
    """
    maps path/url for static content to categories
    """

    title = models.CharField('Title', max_length=100)
    url_path = models.CharField('URL Path', max_length=100,
        help_text="The relative URL path for the content you are wrapping. Can contain letters, numbers, and a forward slash (/). Example: dayton/cincinnatireds")
    originating_site = models.ForeignKey(Site, default=settings.SITE_ID)
    metadata = jsonfield.JSONField(blank=True, default='{"category_slug" : "/news/opinion-blogs", "content_type": "blog"}')

    class Meta:
        unique_together = (('url_path', 'originating_site'),)

    def __unicode__(self):
        """ Who am I?!?! """
        return u"{0} '{1}'".format(self.title, self.url_path)
