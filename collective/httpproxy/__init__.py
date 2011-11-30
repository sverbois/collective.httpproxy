# -*- coding: utf-8 -*-

from zope.i18nmessageid import MessageFactory

HTTPProxyMessageFactory = MessageFactory('collective.httpproxy')


def initialize(context):

    from collective.httpproxy import config
    from collective.httpproxy import httpproxy
    from Products.Archetypes import atapi
    from Products.CMFCore import utils

    content_types, constructors, ftis = atapi.process_types(
        atapi.listTypes(config.PROJECT_NAME),
        config.PROJECT_NAME)

    for atype, constructor in zip(content_types, constructors):
        utils.ContentInit('%s: %s' % (config.PROJECT_NAME, atype.portal_type),
            content_types=(atype, ),
            permission=config.ADD_PERMISSIONS[atype.portal_type],
            extra_constructors=(constructor,),
            ).initialize(context)
