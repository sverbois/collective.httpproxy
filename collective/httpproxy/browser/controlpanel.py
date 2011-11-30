# -*- coding: utf-8 -*-

from collective.httpproxy import HTTPProxyMessageFactory as _
from collective.httpproxy.interfaces import IHTTPProxySettings
from plone.app.registry.browser.controlpanel import RegistryEditForm
from plone.app.registry.browser.controlpanel import ControlPanelFormWrapper
from plone.z3cform import layout


class HTTPProxyControlPanelForm(RegistryEditForm):
    schema = IHTTPProxySettings

HTTPProxyControlPanelView = layout.wrap_form(HTTPProxyControlPanelForm, ControlPanelFormWrapper)
HTTPProxyControlPanelView.label = _(u"HTTP Proxy settings")
