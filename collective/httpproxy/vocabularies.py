# -*- coding: utf-8 -*-

from plone.registry.interfaces import IRegistry
from zope.component import getUtility
from zope.schema.vocabulary import SimpleVocabulary


def EncodingsVocabularyFactory(context):
    """Vocabulary factory for proxied content encodings"""
    registry = getUtility(IRegistry)
    encodings = registry['collective.httpproxy.encodings']
    return SimpleVocabulary.fromValues(encodings)
