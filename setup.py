# -*- coding: utf-8 -*-

from setuptools import setup, find_packages, Extension
from os.path import join

name = 'dolmen.resources'
version = '0.1'
readme = open(join('src', 'dolmen', 'resources', "README.txt")).read()
history = open(join('docs', 'HISTORY.txt')).read()

install_requires = [
    'dolmen.viewlet',
    'fanstatic',
    'setuptools',
    'zope.schema',
    'grokcore.component',
    'zope.i18nmessageid',
    ]

tests_require = [
    'grokcore.component',
    'pytest',
    'zope.component [test]',
    'cromlech.browser [test]',
    'webob',
    'zope.testing',
    'WebTest',
    ]

setup(name = name,
      version = version,
      description = 'Dolmen resources components',
      long_description = readme + '\n\n' + history,
      keywords = 'Dolmen resources implementation.',
      author = 'Souheil Chelfouh',
      author_email = 'trollfot@gmail.com',
      url = '',
      license = 'ZPL',
      classifiers = [
        'Environment :: Web Environment',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        ],
      packages=find_packages('src', exclude=['ez_setup']),
      package_dir={'': 'src'},
      namespace_packages = ['dolmen'],
      include_package_data = True,
      platforms = 'Any',
      zip_safe = False,
      tests_require = tests_require,
      install_requires = install_requires,
      extras_require = {
          'test': tests_require,
          },
      )
