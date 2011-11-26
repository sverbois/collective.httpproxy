import unittest2 as unittest
from zope.component import getUtility
from plone.registry.interfaces import IRegistry

from collective.httpproxy.testing import HTTP_PROXY_FUNCTIONAL_TESTING


class TestSetup(unittest.TestCase):

    layer = HTTP_PROXY_FUNCTIONAL_TESTING

    def test_settings_installed(self):
        registry = getUtility(IRegistry)
        self.assertTrue('collective.httpproxy.encodings' in registry)
        self.assertTrue('collective.httpproxy.proxyExceptions' in registry)
        self.assertTrue('collective.httpproxy.socketTimeout' in registry)
