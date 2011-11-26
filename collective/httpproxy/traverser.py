# -*- coding: utf-8 -*-

from plone.registry.interfaces import IRegistry
from zope.component import getMultiAdapter, getUtility
from zExceptions import NotFound
from ZPublisher.BaseRequest import DefaultPublishTraverse


class HTTPProxyPublishTraverse(DefaultPublishTraverse):

    def publishTraverse(self, request, name):
        registry = getUtility(IRegistry)
        if name in registry['collective.httpproxy.proxyExceptions']:
            return super(HTTPProxyPublishTraverse, self).publishTraverse(request, name)
        else:
            subpath_segments = [name] + request.get('TraversalRequestNameStack')
            request['TraversalRequestNameStack'] = []
            request.remote_subpath = '/'.join(subpath_segments)
            return getMultiAdapter((self.context, request), name=u'httpproxy_view')
