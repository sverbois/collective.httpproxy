# -*- coding: utf-8 -*-

from zope.interface import implements

from Products.Archetypes import atapi
from Products.ATContentTypes.content import link

from Products.DataGridField import DataGridField, DataGridWidget
from Products.DataGridField.Column import Column

from collective.httpproxy import HTTPProxyMessageFactory as _
from collective.httpproxy.config import PROJECT_NAME
from collective.httpproxy.interfaces import IHTTPProxy


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
    DataGridField('tagSelection',
            columns=("urlStart", "beginTag", "endTag"),
            widget = DataGridWidget(
                label=_(u"Content selection"),
                description=_(u"Select part of content you want to get, based on remote URL"),
                columns={
                    'urlStart': Column(_(u"URL starts with")),
                    'beginTag': Column(_(u"Content start tag")),
                    'endTag': Column(_(u"Content end tag"))
                },
             ),
     ),
))


class HTTPProxy(link.ATLink):
    """HTTP Proxy Content Type"""
    implements(IHTTPProxy)

    meta_type = "HTTPProxy"
    schema = HTTPProxySchema

atapi.registerType(HTTPProxy, PROJECT_NAME)
