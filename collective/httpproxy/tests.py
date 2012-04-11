import unittest2 as unittest
from zope.component import getUtility, getMultiAdapter
from zope.component.interfaces import ComponentLookupError
from zope.interface import alsoProvides
from plone.testing.z2 import Browser
from plone.app.testing import setRoles, TEST_USER_ID
from plone.registry.interfaces import IRegistry

from collective.httpproxy.interfaces import IHTTPProxySettings, ILayerSpecific
from collective.httpproxy.testing import HTTP_PROXY_FUNCTIONAL_TESTING, \
                                         HTTP_PROXY_INTEGRATION_TESTING
from collective.httpproxy.browser.httpproxyview import DummyResponse, HTTPProxyView

TEST_HTML_PAGE = u"""
<html>
    <body>
        <h1 id="test-title">Test page title</h1>
        <p></p>
    </body>
</html>
"""


def _get_remote_content(self):
    resp = DummyResponse()
    resp.status = 200
    resp.get = lambda x: 'text/html' if x == 'content-type' else None
    return resp, TEST_HTML_PAGE


class BaseTestCase(unittest.TestCase):

    def setUp(self):
        portal = self.layer['portal']
        if not 'test' in portal.objectIds():
            setRoles(portal, TEST_USER_ID, ('Manager', ))
            portal.invokeFactory('HTTPProxy', 'test',
                                 title=u'Test Proxy',
                                 remoteUrl='http://test-url-for-proxy.org',
                                 encoding='utf8',
                                 tagsSelections=[{'urlStart': '',
                                                'beginTag': '',
                                                'endTag': ''},
                                                {'urlStart': 'search.php',
                                                'beginTag': '<p>',
                                                'endTag': '</p>'},
                                                {'urlStart': 'search',
                                                'beginTag': '<h1 id="test-title">',
                                                'endTag': '</h1>'}])
            portal.invokeFactory('HTTPProxy', 'testempty',
                                 title=u'Test Empty Tags Proxy',
                                 remoteUrl='http://test-url-for-proxy.org',
                                 encoding='iso-8859-15',
                                 tagsSelections=[])
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

    def test_product_installed(self):
        portal = self.layer['portal']
        pq = portal['portal_quickinstaller']
        self.assertTrue(pq.isProductInstalled('collective.httpproxy'))


class TestProxyView(BaseTestCase):

    layer = HTTP_PROXY_INTEGRATION_TESTING

    def test_view_available(self):
        portal = self.layer['portal']
        request = self.layer['request']
        with self.assertRaises(ComponentLookupError):
            getMultiAdapter((portal, request), name=u'httpproxy_view')
        alsoProvides(request, ILayerSpecific)
        with self.assertRaises(ComponentLookupError):
            getMultiAdapter((portal, request), name=u'httpproxy_view')
        self.assertIsNotNone(getMultiAdapter((portal.test, request), name=u'httpproxy_view'))

    def test_construct_request_params(self):
        portal = self.layer['portal']
        request = self.layer['request']
        request.remote_subpath = 'test.php'
        alsoProvides(request, ILayerSpecific)
        view = getMultiAdapter((portal.test, request), name=u'httpproxy_view')
        url, params = view._construct_request_params()
        self.assertEqual(url, 'http://test-url-for-proxy.org/test.php')
        self.assertDictEqual(params, {'method': 'GET',
                                      'body': None,
                                      'headers': {'Content-Type': 'text/html; charset=utf-8'}})

        request.form = {'page_id': 1,
                        'section_id': 'foo'}
        view = getMultiAdapter((portal.test, request), name=u'httpproxy_view')
        url, params = view._construct_request_params()
        self.assertEqual(url, 'http://test-url-for-proxy.org/test.php?page_id=1&section_id=foo')
        self.assertDictEqual(params, {'method': 'GET',
                                      'body': None,
                                      'headers': {'Content-Type': 'text/html; charset=utf-8'}})

        request.form = {}
        request.environ['REQUEST_METHOD'] = 'POST'
        view = getMultiAdapter((portal.test, request), name=u'httpproxy_view')
        url, params = view._construct_request_params()
        self.assertEqual(url, 'http://test-url-for-proxy.org/test.php')
        self.assertDictEqual(params, {'method': 'POST',
                                      'body': None,
                                      'headers': {'Content-Type': 'text/html; charset=utf-8'}})

        request.form = {'page_id': 1,
                        'section_id': 'foo'}
        view = getMultiAdapter((portal.test, request), name=u'httpproxy_view')
        url, params = view._construct_request_params()
        self.assertEqual(url, 'http://test-url-for-proxy.org/test.php')
        self.assertDictEqual(params, {'method': 'POST',
                                      'body': 'page_id=1&section_id=foo',
                                      'headers': {'Content-Type': 'application/x-www-form-urlencoded'}})

    def test_find_tags_to_match(self):
        portal = self.layer['portal']
        request = self.layer['request']

        request.remote_subpath = ''
        view = HTTPProxyView(portal.test, request)
        beginTag, endTag = view._find_tags_to_match()
        self.assertEqual(beginTag, '')
        self.assertEqual(endTag, '')

        request.remote_subpath = 'test.php'
        view = HTTPProxyView(portal.test, request)
        beginTag, endTag = view._find_tags_to_match()
        self.assertEqual(beginTag, '')
        self.assertEqual(endTag, '')

        request.remote_subpath = 'search.php?param1=foo&param2=bar'
        view = HTTPProxyView(portal.test, request)
        beginTag, endTag = view._find_tags_to_match()
        self.assertEqual(beginTag, '<p>')
        self.assertEqual(endTag, '</p>')

        request.remote_subpath = 'search?param1=foo'
        view = HTTPProxyView(portal.test, request)
        beginTag, endTag = view._find_tags_to_match()
        self.assertEqual(beginTag, '<h1 id="test-title">')
        self.assertEqual(endTag, '</h1>')

        request.remote_subpath = 'test'
        view = HTTPProxyView(portal.testempty, request)
        beginTag, endTag = view._find_tags_to_match()
        self.assertEqual(beginTag, '')
        self.assertEqual(endTag, '')

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
