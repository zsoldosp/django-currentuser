=============================
django-currentuser
=============================

.. contents:: Conveniently store reference to request user on thread/db level.

Quickstart
----------

Install django-currentuser::

    pip install django-currentuser

Add it to the middleware classes in your settings.py::

    MIDDLEWARE = (
        ...,
        'django_currentuser.middleware.ThreadLocalUserMiddleware',
    )

Then use it in a project::

    from django_currentuser.middleware import (
        get_current_user, get_current_authenticated_user)

    # As model field:
    from django_currentuser.db.models import CurrentUserField
    class Foo(models.Model):
        created_by = CurrentUserField()
        updated_by = CurrentUserField(on_update=True)


Differences to django-cuser
---------------------------

Both libraries serve the same purpose, but be aware of these
differences (as of django-cuser v.2017.3.16):

- django-currentuser's CurrentUserField stores the reference to the request user
  at initialization of the model instance and still allows you to overwrite the
  value before saving. django-cuser sets the value in the pre_save handler
  of the field just before writing it to the database. Intermediate changes
  will be ignored.

- django-cuser deletes the user reference from the thread after finishing a
  response and it will therefore no longer be available for testing purposes.

Supported Versions
------------------
* for django-currentuser`, fixes are always made against the latest version
* for Python, support is guided by https://devguide.python.org/versions/#supported-versions
* for Django, support is guided by
  https://docs.djangoproject.com/en/dev/faq/install/#what-python-version-can-i-use-with-django
  and https://www.djangoproject.com/download/#supported-versions (assuming the Python version
  listed there is supported)

Release Notes
-------------

* 0.7.0
  * add support for Django 5.0
  * add support for Python 3.12
  * drop support for Django 4.0 and 4.1
* 0.6.1

  * remove project transfer warning from README in order not to scare people away from the project

* 0.6.0

  * add support for Django 4.0, 4.1, and 4.2
  * add support for Python 3.11
  * drop support for Python 3.6 and 3.7

* 0.5.3 - add support for Django 3.2 and Python 3.9

* 0.5.2 - Fixed Django deprecation warning about using `ugettext_lazy()`

* 0.5.1 - add support for Django 3.1 and Python 3.8

* 0.5.0
  - add support for update on save (thank you @felubra)
  - no longer build on Python 3.5, deprecated

* 0.4.3 - add support for Django 3.0

* 0.4.2 - Minor fix for supported Django and Python versions

* 0.4.0 - update supported versions

  - drop support for Python 3.4
  - drop support for Django 2.0
  - add support for Python 3.7
  - add support for Django 2.2
  - update tox3travis.py to not loose deployment feature

* 0.3.4 - Use public Travis for packaging to remove dependency on outdated build
  system
* 0.3.3 - drop Python 3.7 support due to build process problems
* 0.3.1 - attempt to add Python 3.7 support
* 0.3.0 - update supported versions according to
  https://www.djangoproject.com/download/#supported-versions and
  https://devguide.python.org/#status-of-python-branches

  - drop support for Python 3.2

* 0.2.3 - support custom user model, drop Django 1.10 support
* 0.2.2 - support Django 2.0
* 0.2.1 - version fixes #9

  - support Django 1.11.x and not just 1.11.0

* 0.2.0 - New middleclass format

  - Adapt to new object based middle class format of Django 1.10+
  - Drop support for deprecated Django versions 1.8 and 1.9

* 0.1.1 - minor release

  - suppress warning for passed kwargs as long as they match the defaults (avoids them being printed during running tests when fields are cloned)

* 0.1.0 - initial release

  - provides middleware + methods to set + retrieve reference of currently logged in user from thread
  - provides CurrentUserField that by default stores the currently logged in user
  - supports Django 1.10, 1.11 on python 2.7, 3.4, 3.5, and 3.6 - as per the `official django docs <https://docs.djangoproject.com/en/dev/faq/install/#what-python-version-can-i-use-with-django>`_


.. contributing start

Contributing
------------

As an open source project, we welcome contributions.

The code lives on `github <https://github.com/zsoldosp/django-currentuser>`_.

Reporting issues/improvements
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Please open an `issue on github <https://github.com/zsoldosp/django-currentuser/issues/>`_
or provide a `pull request <https://github.com/zsoldosp/django-currentuser/pulls/>`_
whether for code or for the documentation.

For non-trivial changes, we kindly ask you to open an issue, as it might be rejected.
However, if the diff of a pull request better illustrates the point, feel free to make
it a pull request anyway.

Pull Requests
~~~~~~~~~~~~~

* for code changes

  * it must have tests covering the change. You might be asked to cover missing scenarios
  * the latest ``flake8`` will be run and shouldn't produce any warning
  * if the change is significant enough, documentation has to be provided

To trigger the packaging, run `make release` on the master branch with a changed
version number.

Setting up all Python versions
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

::

    sudo apt-get -y install software-properties-common
    sudo add-apt-repository ppa:fkrull/deadsnakes
    sudo apt-get update
    for version in 3.8 3.9 3.10 3.11; do
      py=python$version
      sudo apt-get -y install ${py} ${py}-dev
    done

Code of Conduct
~~~~~~~~~~~~~~~

As it is a Django extension, it follows
`Django's own Code of Conduct <https://www.djangoproject.com/conduct/>`_.
As there is no mailing list yet, please use `github issues`_

Contributors
~~~~~~~~~~~~
Current maintainer: @zsoldosp
Initial development & maintenance: @PaesslerAG

For contributors, see `github contributors`_.


.. contributing end


.. _github contributors: https://github.com/zsoldosp/django-currentuser/graphs/contributors
.. _github issues: https://github.com/zsoldosp/django-currentuser/issues
