# -*- coding: utf-8 -*-

from plone.registry.interfaces import IRegistry
from zope.component import getMultiAdapter, getUtility
from ZPublisher.BaseRequest import DefaultPublishTraverse
from collective.httpproxy.interfaces import IHTTPProxySettings


class HTTPProxyPublishTraverse(DefaultPublishTraverse):

    def publishTraverse(self, request, name):
        settings = getUtility(IRegistry).forInterface(IHTTPProxySettings)
        if name in settings.proxyExceptions:
            return super(HTTPProxyPublishTraverse, self).publishTraverse(request, name)
        else:
            subpath_segments = [name] + request.get('TraversalRequestNameStack')
            request['TraversalRequestNameStack'] = []
            request.remote_subpath = '/'.join(subpath_segments)
            return getMultiAdapter((self.context, request), name=u'httpproxy_view')
