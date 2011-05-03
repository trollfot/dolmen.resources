# -*- coding: utf-8 -*-

import pytest
import webob
from webob.dec import wsgify
from grokcore.component import testing
from fanstatic import Library, Resource, get_needed, NEEDED, Injector
from dolmen.resources import ResourcesManager, ResourceViewlet
from dolmen.viewlet import slot, view
from zope.testing.cleanup import cleanUp


class MyView(object):

    def __init__(self, context, request):
        self.context = context
        self.request = request
 
    def render(self):
        return u"<html><head></head><body>a simple view</body></html>" % (
            self.context)


class Resources(ResourcesManager):
    pass


class MyApp(object):

    def __init__(self, context, view):
        self.context = context
        self.view = view

    @wsgify
    def __call__(request):

        # configuration
        needed = get_needed()
        needed.base_url = 'http://testapp'

        # Resource viewlets
        view = self.view(self.context, request)
        manager = Resources(self.context, request, view)
        manager()
        return [view.render()]


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

    testing.grok_component('myresources', MyResources)
    wrapped_app = Injector(MyApp(object(), MyView))
    request = webob.Request.blank('/')
    response = request.get_response(wrapped_app)
    assert response.body == 'toto'
