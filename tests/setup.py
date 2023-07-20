#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

if sys.argv[-1] in ('publish', 'release'):
    raise Exception('this is a test app, do not release it!')

readme = 'A simple test application to test django_currentuser'

setup(
    name='testapp',
    version='0.0.0',
    description=readme,
    long_description=readme,
    packages=[
        'testapp',
    ],
    include_package_data=True,
    install_requires=[
    ],
    license="BSD",
    zip_safe=False,
    keywords='django-currentuser-test-app',
)
