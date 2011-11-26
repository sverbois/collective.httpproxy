# -*- coding: utf-8 -*-

from setuptools import setup, find_packages
import os

version = '0.1dev'

setup(name='collective.httpproxy',
      version=version,
      description="collective.httpproxy add the archetype content type 'HTTP Proxy' into Plone",
      long_description=open('README.rst').read() +
        open(os.path.join('docs', 'HISTORY.txt')).read(),
      classifiers=[
        "Framework :: Plone",
        "Framework :: Plone :: 4.1",
        "Programming Language :: Python",
      ],
      keywords='plone content',
      author='Sébastien Verbois',
      author_email='sebastien.verbois@gmail.com',
      url='https://github.com/sverbois/collective.httpproxy',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['collective'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
            'setuptools',
            'plone.app.registry',
            'httplib2',
      ],
      extras_require={
            'test': ['plone.app.testing',]
      },
      entry_points="""
      # -*- Entry points: -*-
      [z3c.autoinclude.plugin]
      target = plone
      """,
      )
