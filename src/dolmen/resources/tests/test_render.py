# -*- coding: utf-8 -*-

import pytest
from cromlech.io.testing import TestRequest, TestResponse
from cromlech.browser.testing import TestView, XMLDiff
from cromlech.browser import IView
from zope.interface import implements
from dolmen.resources import ResourcesManager, ResourceViewlet
from dolmen.viewlet import slot, view
from fanstatic import Library, Resource, get_needed, NEEDED, Injector
from grokcore.component import testing
from zope.testing.cleanup import cleanUp
from webtest import TestApp


class MyView(TestView):
    implements(IView)

    def render(self):
        return "<html><head></head><body>A view</body></html>"


class AnotherView(TestView):
    implements(IView)

    def render(self):
        return "<html><head></head><body>A view</body></html>"


class Resources(ResourcesManager):
    pass


class MyApp(object):

    def __init__(self, context, view):
        self.context = context
        self.view = view

    def __call__(self, environ, start_response):
        start_response('200 OK', [])

        # configuration
        needed = get_needed()
        needed.base_url = 'http://testapp'

        # Resource viewlets
        request = TestRequest()
        view = self.view(self.context, request)

        manager = Resources(self.context, request, view)
        manager()
        return view()


def setup_module(module):
    """ grok the publish module
    """
    testing.grok("dolmen.viewlet.meta")


def teardown_module(module):
    """ undo groking
    """
    cleanUp()


def test_inject():

    foo = Library('foo', '')
    x1 = Resource(foo, 'a.js')
    x2 = Resource(foo, 'b.css')

    class MyResources(ResourceViewlet):
        view(MyView)
        slot(Resources)
        resources = [x1, x2]

    expected = '''<html><head>
         <link rel="stylesheet" type="text/css"
               href="http://testapp/fanstatic/foo/b.css" />
         <script type="text/javascript"
               src="http://testapp/fanstatic/foo/a.js"></script>
         </head><body>A view</body></html>'''

    testing.grok_component('myresources', MyResources)
    
    app = TestApp(Injector(MyApp(object(), MyView)))
    res = app.get('/')
    assert XMLDiff(res.body, expected) is None

    app = TestApp(Injector(MyApp(object(), AnotherView)))
    res = app.get('/')
    assert res.body == '<html><head></head><body>A view</body></html>'
