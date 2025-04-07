#!/usr/bin/env python
# -*- coding: utf-8 -*-
from setuptools import setup
import os

use_unsupported_django = os.environ.get('DJANGO_CURRENTUSER_USE_UNSUPPORTED_DJANGO', '0') == '1'

dependencies = ['Django'] if use_unsupported_django else ["Django>=4.2, <6.0"]


if __name__ == "__main__":
    setup(install_requires=dependencies)
