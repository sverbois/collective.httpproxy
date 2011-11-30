Description
===========

*collective.httpproxy* is a Plone product which adds an archetypes content
type 'HTTP Proxy'.

With an 'HTTP Proxy' content, you can proxy an HTTP application (PHP, Pyramid,
...) through a Plone portal.


Installation
============

Dependencies
------------

**plone.app.registry**
    http://pypi.python.org/pypi/plone.app.registry (included in Plone >= 4.1)

**httplib2**    
    http://pypi.python.org/pypi/httplib2

**Products.DataGridField**
    http://pypi.python.org/pypi/Products.DataGridField


Usage
=====

After *collective.httpproxy* installation, you can add an 'HTTP Proxy' just
as any other Plone content. For every 'HTTP Proxy' you need, you can configure
the URL of an external website (or web application) and it's encoding.

Optionnaly, you can also configure which part of the external HTML content you
want to display into your Plone site, by configuring a list of triplets rules : 

1. External URL starts with
2. Content part start tag for this URL
3. Content part end tag for this URL

More specific rules (longuest URL part) take precedence.

Note that 'HTTP Proxy' is not a full-featured proxy, and it may be better if
you have some control over the proxied application :

- URL should always be relative
- tags structure should be clean and useful


Credits
=======

Authors
-------

- Sébastien VERBOIS aka sverbois - sebastien.verbois@gmail.com
- Laurent LASUDRY aka laz - laurent.lasudry@affinitic.be

Contributors
------------
