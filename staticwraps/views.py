"""
staticwraps.views

render out static content
"""

import os
import re

from BeautifulSoup import BeautifulSoup

from django.conf import settings
from django.contrib.sites.models import Site
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from django.http import Http404, HttpResponse
from django.template import loader, RequestContext

from staticwraps.models import StaticWrap


def render_content(request, url_path):
    """
    Given a url path that maps to a local directory, read in and display html content
    """
    base_path = getattr(settings, 'STATICWRAPS_BASE_PATH', None)
    if not base_path:
        raise Http404("No STATICWRAPS_BASE_PATH in settings")

    site = Site.objects.get_current()

    ## fetch the staticwrap object mapped to this url
    m = re.match('^(\w+\/\w+)\/*', url_path)
    if m is not None:
        try:
            staticwrap = StaticWrap.objects.get(url_path=m.group(1))
        except ObjectDoesNotExist:
            raise Http404("StaticWrap matching '%s' does not exist" % url_path)
        except MultipleObjectsReturned:
            staticwrap = StaticWrap.objects.filter(url_path=m.group(1))[0]

    ## read in a html file from base_path matching url_path
    if not re.search(r'\.html$', url_path):
        url_path = url_path + '/index.html'

    ## open our file and read the contents
    file_path = os.path.join(base_path, url_path)

    if not os.path.exists(file_path):
        raise Http404("Blog does not exist: %s" % url_path)

    with open(file_path, 'r') as html_file:
        ## Let BS do a little html cleanup for us
        static_content = BeautifulSoup(html_file.read())

        ## Remove some elements that we don't need or want
        if static_content.head != None:
            head = static_content.head
            head.extract()

        if static_content.script != None:
            script = static_content.script
            script.extract()

        # broken html cleanup hack
        buttons = static_content.findAll(type="button", value="Report abuse")
        [button.extract() for button in buttons]

        clean_content = static_content.prettify()

        # broken html cleanup hack
        clean_content = re.sub('\'\)\" style=\"float:right;\" \/\>', '', clean_content)

        context = {
            "static_content": clean_content,
            "staticwrap": staticwrap,
            "site": site,
            "_ad_target_object": staticwrap,
        }
        c = RequestContext(request, context)
        t = loader.get_template('staticwraps/staticwrap.html')
        response = HttpResponse(t.render(c))
        return response


def render_simple_content(request, url_path):
    """
    Given a url path that maps to a local directory, read in and display raw content
    """
    base_path = getattr(settings, 'STATICWRAPS_BASE_PATH', None)
    if not base_path:
        raise Http404("No STATICWRAPS_BASE_PATH in settings")

    ## open our file and read the contents
    file_path = os.path.join(base_path, url_path)

    if not os.path.exists(file_path):
        raise Http404("url does not exist: %s" % url_path)

    with open(file_path, 'r') as in_file:
        ## Just read in the file contents and push it out dirty as it is
        static_content = in_file.read()

        t = loader.get_template('staticwraps/simplewrap.html')
        c = RequestContext(request, {'static_content': static_content})

        response = HttpResponse(t.render(c), content_type="text/xml")
        return response
