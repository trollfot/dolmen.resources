# -*- coding: utf-8 -*-

from grokcore.component import baseclass
from dolmen.viewlet import slot
from dolmen.viewlet.components import ViewletManager, Viewlet
from dolmen.viewlet.interfaces import IViewlet
from fanstatic import Resource
from zope.schema import List
from zope.interface import implements
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
    baseclass()

    def __init__(self, context, request, view):
        ViewletManager.__init__(self, context, request, view)
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
    baseclass()
    slot(ResourcesManager)
    implements(IResourceViewlet)

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
