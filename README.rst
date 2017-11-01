=============================
django-currentuser
=============================

.. image:: https://travis-ci.org/PaesslerAG/django-currentuser.svg?branch=master
        :target: https://travis-ci.org/PaesslerAG/django-currentuser

----

.. contents:: Conveniently store reference to request user on thread/db level.

----

Quickstart
----------

Install django-currentuser::

    pip install django-currentuser

Add it to the middleware classes in your settings.py::

    MIDDLEWARE_CLASSES = (
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

Release Notes
-------------

* 0.1.1 - minor release

  * suppress warning for passed kwargs as long as they match the defaults (avoids them being printed during running
    tests when fields are cloned)

* 0.1.0 - initial release

  * provides middleware + methods to set + retrieve reference of currently logged in user from thread
  * provides CurrentUserField that by default stores the currently logged in user
  * supports Django 1.8, 1.9, 1.10, 1.11 on python 2.7, 3.3, 3.4, 3.5, and 3.6 - as per the
    `official django docs <https://docs.djangoproject.com/en/dev/faq/install/#what-python-version-can-i-use-with-django>`_


.. contributing start

Contributing
------------

As an open source project, we welcome contributions.

The code lives on `github <https://github.com/PaesslerAG/django-currentuser>`_.

Reporting issues/improvements
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Please open an `issue on github <https://github.com/PaesslerAG/django-currentuser/issues/>`_
or provide a `pull request <https://github.com/PaesslerAG/django-currentuser/pulls/>`_
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

Setting up all Python versions
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

::

    sudo apt-get -y install software-properties-common
    sudo add-apt-repository ppa:fkrull/deadsnakes
    sudo apt-get update
    for version in 3.3 3.5 3.6; do
      py=python$version
      sudo apt-get -y install ${py} ${py}-dev
    done

Code of Conduct
~~~~~~~~~~~~~~~

As it is a Django extension, it follows
`Django's own Code of Conduct <https://www.djangoproject.com/conduct/>`_.
As there is no mailing list yet, please just email one of the main authors
(see ``setup.py`` file or `github contributors`_)


.. contributing end


.. _github contributors: https://github.com/PaesslerAG/django-currentuser/graphs/contributors
