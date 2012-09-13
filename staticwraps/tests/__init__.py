import re
import os

from mock import Mock

from django.conf import settings
from django.contrib.sites.models import Site
from django.http import Http404
from django.test import TestCase

from staticwraps.models import StaticWrap
from staticwraps.views import render_content, render_simple_content


class TestView(TestCase):
    """ test staticwraps views """

    def setUp(self):
        self.site = Site.objects.create(domain="site1.com", name="Site 1")
        self.category_slug = u'opinion-blogs'
        self.staticwrap = StaticWrap.objects.create(title="test",
                url_path="testdata/blog",
                originating_site=self.site,
                metadata='{"category_slug": "%s"}' % self.category_slug,
            )
        self.request = Mock()
        self.request.META = {'HTTP_HOST': 101, 'PATH_INFO': '', 'QUERY_STRING': ''}
        project_root = os.path.dirname(os.path.abspath(__file__))
        settings.STATICWRAPS_BASE_PATH = project_root
        self.old_template_dirs = settings.TEMPLATE_DIRS
        settings.TEMPLATE_DIRS = (os.path.join(project_root, 'templates'),)

    def tearDown(self):
        settings.TEMPLATE_DIRS = self.old_template_dirs

    def testRenderContentView(self):
        """ test staticwraps.views.render_content """

        result = render_content(self.request, 'testdata/blog')
        self.assertIn('My HTML Content', str(result))
        self.assertIn('name="category_slug" content="opinion-blogs"', str(result))
        self.assertIn('name="title" content="test"', str(result))

    def testNoStaticWrap(self):
        """ should raise a 404 if matching staticwrap doesn't exist """
        with self.assertRaises(Http404):
            render_content(self.request, 'testdata/foo')

    def testBadUrlPath(self):
        """ should raise a 404 if staticwrap exists, but path doesn't exist """
        StaticWrap.objects.create(title="test",
                url_path="testdata/foo",
                originating_site=self.site,
                metadata='{"category_slug": "foo-slug"}',
            )
        with self.assertRaises(Http404):
            render_content(self.request, 'testdata/foo')

    def testCleanHtmlContent(self):
        """ make sure the stuff we don't want is gone """

        result = render_content(self.request, 'testdata/blog')
        self.assertNotIn('<head>FOO</head>', str(result))
        self.assertNotIn('<!--#echo var="SITENAME_GENNI"-->', str(result))

    def testRenderSimpleContentView(self):
        """ test staticwraps.views.render_simple_content """

        result = render_simple_content(self.request, 'testdata/blog/simple.xml')

        assert re.search(r'^Content-Type: text\/xml\n\nMy XML Content$', str(result)) != None
