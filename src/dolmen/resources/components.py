# -*- coding: utf-8 -*-

import grokcore.component as grok
from dolmen.viewlet.components import ViewletManager, Viewlet
from dolmen.viewlet.interfaces import IViewlet
from dolmen.viewlet.manager import ViewletManagerBase
from fanstatic import Resource
from zope.schema import List
from zope.schema.fieldproperty import FieldProperty


class IResourceViewlet(IViewlet):
    """A viewlet which sole purpose is to include resources.
    """
    resources = List(
        title=u"Resources to be included",
        required=True)

    def render(self):
        """Calling this method will include the resources.
        The return value will *not* be taken in consideration.
        """


class ResourcesManager(ViewletManager):
    """A manager which sole purpose is to render ResourceViewlets.
    """
    grok.baseclass()

    def __init__(self, context, request, view):
        ViewletManagerBase.__init__(self, context, request, view)
        self.context = context
        self.request = request
        self.view = view

    def sort(self, viewlets):
        return viewlets

    def namespace(self):
        raise NotImplementedError(
            "No template can be associated to this component")

    def render(self):
        for viewlet in self.viewlets:
            if IResourceViewlet.providedBy(viewlet):
                viewlet.render()


class ResourceViewlet(Viewlet):
    """A viewlet including resources.
    """
    grok.baseclass()
    grok.implements(IResourceViewlet)
    grok.viewletmanager(ResourcesManager)

    resources = FieldProperty(IResourceViewlet['resources'])

    def __init__(self, context, request, view, manager):
        pass

    def namespace(self):
        raise NotImplementedError(
            "No template can be associated to this component")

    def update(self):
        pass

    def render(self):
        for resource in self.resources:
            if isinstance(resource, Resource):
                resource.need()
