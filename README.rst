==============
Aldryn Gallery
==============

.. image:: https://travis-ci.org/aldryn/aldryn-gallery.svg?branch=master
    :target: https://travis-ci.org/aldryn/aldryn-gallery

.. image:: https://img.shields.io/coveralls/aldryn/aldryn-gallery.svg
  :target: https://coveralls.io/r/aldryn/aldryn-gallery


Aldryn Gallery is build on the principle of plugin-in-plugin provided by django-cms 
since version 3.0.

Installation
============

::

    pip install aldryn-gallery

Add ``aldryn_gallery`` to ``INSTALLED_APPS``.

Configure ``aldryn-boilerplates`` (https://pypi.python.org/pypi/aldryn-boilerplates/).

To use the old templates, set ``ALDRYN_BOILERPLATE_NAME='legacy'``.
To use https://github.com/aldryn/aldryn-boilerplate-standard (recommended, will be renamed to
``aldryn-boilerplate-bootstrap3``) set ``ALDRYN_BOILERPLATE_NAME='bootstrap3'``.

When using the ``legacy`` boilerplate, **jQuery** and
`classjs <https://github.com/finalangel/classjs-plugins>`_ cl.gallery are required.
