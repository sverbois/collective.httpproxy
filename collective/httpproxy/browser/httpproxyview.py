# -*- coding: utf-8 -*-

import httplib2
import re
import urllib

from plone.registry.interfaces import IRegistry
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from socket import timeout as SocketTimeout
from zope.component import getUtility
from zope.publisher.browser import BrowserView
from collective.httpproxy.interfaces import IHTTPProxySettings


class HTTPProxyView(BrowserView):
    """
    """

    index = ViewPageTemplateFile("httpproxyview.pt")
    
    def __init__(self, context, request):
        super(HTTPProxyView, self).__init__(context, request)
        self.remote_subpath = getattr(request, 'remote_subpath', '')

    def __call__(self):
        resp, content = self._get_remote_content()
        self.proxy_response = resp
        self.proxy_content = content

        if self.proxy_response.status == 200:
            content_type = self.proxy_response['content-type']
            if 'text/html' in content_type:
                main_proxy_content = self._extract_main_content(self.proxy_content)
                main_content = self._convert_to_utf8(main_proxy_content)
                return self.index(main_content=main_content)
            else:
                self.request.response.setHeader('Content-Type', content_type)
                content_disposition = self.proxy_response.get('content-disposition',None)
                if content_disposition:
                    self.request.response.setHeader('Content-Disposition', content_disposition)
                return self.proxy_content
        else:
            message = u"<p>The application %s is not responding.</p><pre>ERROR %d %s</pre>" %\
                   (self.context.Title(), self.proxy_response.status, self.proxy_response.reason)
            return self.index(main_content=message)

    def _construct_request_params(self):
        url = self.context.getRemoteUrl()
        if self.remote_subpath:
            url = url + '/' + self.remote_subpath
        params = {}
        method = self.request.environ['REQUEST_METHOD']
        form = self.request.form
        body = None
        headers = {'Content-Type': 'text/html; charset=utf-8'}
        #host_header = self.context.absolute_url().split('//')[1]
        #headers['Host'] = host_header
        if method == 'GET' and form:
            url += '?' + urllib.urlencode(form)
        elif method == 'POST' and form:
            headers['Content-Type'] = 'application/x-www-form-urlencoded'
            body = urllib.urlencode(form)
        params['method'] = method
        params['body'] = body
        params['headers'] = headers
        return url, params

    def _get_remote_content(self):
        settings = getUtility(IRegistry).forInterface(IHTTPProxySettings)
        try:
            h = httplib2.Http(timeout=settings.socketTimeout)
            url, params = self._construct_request_params()
            resp, request_content = h.request(url, **params)
            content = request_content if request_content else ''
        except SocketTimeout:
            resp = object()
            resp.status = 504
            resp.reason = 'Gateway Timeout'
            content = ''
        except Exception as e:
            resp = object()
            resp.status = 502
            resp.reason = 'Bad Gateway'
            content = ''
        return resp, content

    def _find_tags_to_match(self):
        tag_selections = self.context.getTagsSelections()
        selected = None
        for possible_match in tag_selections:
            if self.remote_subpath.startswith(possible_match['urlStart']):
                if selected is None or \
                   len(possible_match['urlStart']) >= len(selected['urlStart']):
                    selected = possible_match
        if selected is None:
            return "", ""
        else:
            return selected['beginTag'], selected['endTag']

    def _extract_main_content(self, content):
        begin, end = self._find_tags_to_match()
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
