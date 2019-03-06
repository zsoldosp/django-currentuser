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
        'Django==1.11;python_version<"3.0"',
        'Django>=1.11,<2.1;python_version<"3.5"',
        'Django>=1.11,<2.2;python_version>"3.4"',
    ],
    license="BSD",
    zip_safe=False,
    keywords='django-currentuser',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Framework :: Django',
        'Framework :: Django :: 1.11',
        'Framework :: Django :: 2.0',
        'Framework :: Django :: 2.1'
    ],
)
