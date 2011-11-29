# -*- coding: utf-8 -*-

import httplib2
import re
import urllib

from plone.registry.interfaces import IRegistry
from socket import timeout as SocketTimeout
from zope.component import getUtility
from zope.publisher.browser import BrowserView
from collective.httpproxy.interfaces import IHTTPProxySettings


class HTTPProxyView(BrowserView):
    """
    """

    def __init__(self, context, request):
        self.context = context
        self.request = request
        self.remote_url = context.getRemoteUrl()
        self.remote_subpath = getattr(request, 'remote_subpath', '')
        self.host_header = context.absolute_url().split('//')[1]

    def main_content(self):
        status, reason, content = self._get_remote_content()
        if status == 200:
            main_content = self._extract_main_content(content)
            return self._convert_to_utf8(main_content)
        else:
            return "<p>The application %s is not responding.</p><pre>ERROR %d %s</pre><p>%s<p>" % (self.context.Title(), status, reason, content)

    def _get_remote_content(self):
        settings = getUtility(IRegistry).forInterface(IHTTPProxySettings)
        try:
            h = httplib2.Http(timeout=settings.socketTimeout)
            url = self.remote_url
            if self.remote_subpath:
                url = url + '/' + self.remote_subpath
            method = self.request.environ['REQUEST_METHOD']
            params = self.request.form
            body = None
            headers = {'Content-Type': 'text/html; charset=utf-8'}
            if method == 'GET' and params:
                url += '?' + urllib.urlencode(params)
            elif method == 'POST' and params:
                headers['Content-Type'] = 'application/x-www-form-urlencoded'
                body = urllib.urlencode(params)
            resp, request_content = h.request(url, method=method, body=body,
                                              headers=headers)
            status = resp.status
            reason = resp.reason
            content = request_content if request_content else ''
        except SocketTimeout:
            status = 504
            reason = 'Gateway Timeout'
            content = ''
        except Exception as e:
            status = 502
            reason = 'Bad Gateway'
            content = str(e)
        return status, reason, content

    def find_tags_to_match(self):
        tagSelection = self.context.getTagSelection()
        selected = None
        for possibleMatch in tagSelection:
            if self.remote_subpath.startswith(possibleMatch['urlStart']):
                if selected is None or \
                   len(possibleMatch['urlStart']) >= len(selected['urlStart']):
                    selected = possibleMatch
        if selected is None:
            return "", ""
        else:
            return selected['beginTag'], selected['endTag']

    def _extract_main_content(self, content):
        begin, end = self.find_tags_to_match()
        regexp = re.compile(r"(%s)(.*)(%s)" % (begin, end), re.DOTALL)
        result = regexp.search(content)
        if result:
            main_content = result.group(2)
        else:
            main_content = "ERROR : no section '%s','%s' found in this page." % (begin, end)
        return main_content

    def _convert_to_utf8(self, content):
        encoding = self.context.getEncoding()
        if encoding == 'utf8':
            return content
        else:
            return content.decode(encoding).encode('utf8')
