# -*- coding: utf-8 -*-

from collective.httpproxy.config import PROJECT_NAME
from collective.httpproxy.interfaces import IHTTPProxy
from collective.httpproxy import HTTPProxyMessageFactory as _
from zope.interface import implements
from Products.Archetypes import atapi
from Products.ATContentTypes.content import link


HTTPProxyBaseSchema = link.ATLinkSchema.copy()

HTTPProxySchema = HTTPProxyBaseSchema + atapi.Schema((
    atapi.StringField('encoding',
        required = True,
        vocabulary_factory = "collective.httpproxy.vocabularies.encodings",
        default = 'utf8',
        widget = atapi.SelectionWidget(
            label=_(u"Encoding"),
            description=_(u"Encoding of the proxied content"),
            format='radio'),
    ),
    atapi.StringField('beginTag',
        required = False,
        widget = atapi.StringWidget(
            label=_(u"Content start tag")),
    ),
    atapi.StringField('endTag',
        required = False,
        widget = atapi.StringWidget(
            label=_(u"Content end tag")),
    ),
))


class HTTPProxy(link.ATLink):
    """HTTP Proxy Content Type"""
    implements(IHTTPProxy)

    meta_type = "HTTPProxy"
    schema = HTTPProxySchema

atapi.registerType(HTTPProxy, PROJECT_NAME)
