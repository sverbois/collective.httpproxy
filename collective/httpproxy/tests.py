import unittest2 as unittest
from zope.component import getUtility
from plone.testing.z2 import Browser
from plone.app.testing import setRoles, TEST_USER_ID
from plone.registry.interfaces import IRegistry

from collective.httpproxy.interfaces import IHTTPProxySettings
from collective.httpproxy.testing import HTTP_PROXY_FUNCTIONAL_TESTING, \
                                         HTTP_PROXY_INTEGRATION_TESTING
from collective.httpproxy.browser.httpproxyview import HTTPProxyView

TEST_HTML_PAGE = u"""
<html>
    <body>
        <h1 id="test-title">Test page title</h1>
        <p></p>
    </body>
</html>
"""


def _get_remote_content(self):
    return 200, "", TEST_HTML_PAGE


class BaseTestCase(unittest.TestCase):

    def setUp(self):
        portal = self.layer['portal']
        if not 'test' in portal.objectIds():
            setRoles(portal, TEST_USER_ID, ('Manager', ))
            portal.invokeFactory('HTTPProxy', 'test',
                                 title=u"Test Proxy",
                                 remoteUrl="http://test-url-for-proxy.org",
                                 tagSelection=[{'urlStart': '',
                                                'beginTag': '',
                                                'endTag': ''},
                                                {'urlStart': 'search.php',
                                                'beginTag': '<p>',
                                                'endTag': '</p>'},
                                                {'urlStart': 'search',
                                                'beginTag': '<h1 id="test-title">',
                                                'endTag': '</h1>'}])
            setRoles(portal, TEST_USER_ID, ('Member', ))
            import transaction; transaction.commit()
        self.origMethod = HTTPProxyView._get_remote_content
        HTTPProxyView._get_remote_content = _get_remote_content

    def tearDown(self):
        HTTPProxyView._get_remote_content = self.origMethod


class TestSetup(unittest.TestCase):

    layer = HTTP_PROXY_FUNCTIONAL_TESTING

    def test_settings_installed(self):
        settings = getUtility(IRegistry).forInterface(IHTTPProxySettings)
        self.assertIsNotNone(settings.encodings)
        self.assertIsNotNone(settings.proxyExceptions)
        self.assertIsNotNone(settings.socketTimeout)


class TestProxyView(BaseTestCase):

    layer = HTTP_PROXY_INTEGRATION_TESTING

    def test_find_tags_to_match(self):
        portal = self.layer['portal']
        request = self.layer['request']

        request.remote_subpath = ''
        view = HTTPProxyView(portal.test, request)
        beginTag, endTag = view.find_tags_to_match()
        self.assertEqual(beginTag, '')
        self.assertEqual(endTag, '')

        request.remote_subpath = 'test.php'
        view = HTTPProxyView(portal.test, request)
        beginTag, endTag = view.find_tags_to_match()
        self.assertEqual(beginTag, '')
        self.assertEqual(endTag, '')

        request.remote_subpath = 'search.php?param1=foo&param2=bar'
        view = HTTPProxyView(portal.test, request)
        beginTag, endTag = view.find_tags_to_match()
        self.assertEqual(beginTag, '<p>')
        self.assertEqual(endTag, '</p>')

        request.remote_subpath = 'search?param1=foo'
        view = HTTPProxyView(portal.test, request)
        beginTag, endTag = view.find_tags_to_match()
        self.assertEqual(beginTag, '<h1 id="test-title">')
        self.assertEqual(endTag, '</h1>')

    def test_no_tag_filtering(self):
        app = self.layer['app']
        portal = self.layer['portal']
        browser = Browser(app)
        browser.open(portal.test.absolute_url())
        self.assertTrue(TEST_HTML_PAGE in browser.contents)
        browser.open(portal.test.absolute_url() + '/foo/bar')
        self.assertTrue(TEST_HTML_PAGE in browser.contents)

    def test_tag_filtering(self):
        app = self.layer['app']
        portal = self.layer['portal']
        browser = Browser(app)
        browser.open(portal.test.absolute_url() + '/search')
        self.assertTrue('Test page title' in browser.contents)
        self.assertFalse('<h1 id="test-title">' in browser.contents)
