# -*- coding: utf-8 -*-

from plone.registry.interfaces import IRegistry
from zope.component import getUtility
from zope.schema.vocabulary import SimpleVocabulary
from collective.httpproxy.interfaces import IHTTPProxySettings


def EncodingsVocabularyFactory(context):
    """Vocabulary factory for proxied content encodings"""
    settings = getUtility(IRegistry).forInterface(IHTTPProxySettings)
    encodings = settings.encodings
    return SimpleVocabulary.fromValues(encodings)
