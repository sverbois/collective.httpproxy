# -*- coding: utf-8 -*-

from collective.httpproxy import HTTPProxyMessageFactory as _
from zope import schema
from zope.interface import Interface


class IHTTPProxy(Interface):
    """HTTP Proxy marker interface"""


class ILayerSpecific(Interface):
    """Specific browser layer marker interface"""


class IHTTPProxySettings(Interface):
    """HTTPProxy settings interface"""
    encodings = schema.List(
        title=_(u"Proxied content encodings"),
        value_type=schema.ASCIILine(title=_(u"Encoding"))
    )
    proxyExceptions = schema.List(
        title=_(u"Proxy traversing exceptions"),
        value_type=schema.ASCIILine(title=_(u"Exception"))
    )
    socketTimeout = schema.Float(
        title=_(u"Socket timeout"),
        min=0.0
    )
