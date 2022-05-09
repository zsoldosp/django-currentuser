#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys

import django_currentuser

from setuptools import setup

version = django_currentuser.__version__

if sys.argv[-1] == 'publish':
    os.system('make release')
    sys.exit()

readme = open('README.rst').read()

description = "Conveniently store reference to request user on thread/db level."

setup(
    name='django-currentuser',
    version=version,
    description=description,
    long_description=readme,
    author='Paessler AG',
    author_email='bis@paessler.com',
    url='https://github.com/PaesslerAG/django-currentuser',
    packages=[
        'django_currentuser',
    ],
    include_package_data=True,
    install_requires=[
        'Django>=1.11.17,<5.0;python_version>="2.7"',
    ],
    license="BSD",
    zip_safe=False,
    keywords='django-currentuser',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Framework :: Django',
        'Framework :: Django :: 2.2',
        'Framework :: Django :: 3.0',
        'Framework :: Django :: 3.1',
        'Framework :: Django :: 3.2',
        'Framework :: Django :: 4.0',
    ],
)
