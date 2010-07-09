.. _intro:

Introduction
================================================================================

*KalaPy* is a web application framework for `Python`_ providing it's own
:ref:`Database Abstraction Layer <dal>`, web components based on `Werkzeug`_,
templating using powerful `Jinja2`_ template engine and full :ref:`internationalization <i18n>`
support via `Babel`_ and `pytz`_ and more...

The development is still under alpha stage and API might change during this
period. I welcome your useful suggestions/thoughts about how to improve it and
how it should look like.

At the moment it looks some what similar to `Django`_, but it is only so to get
started quickly. The intention is to implement a framework that combines power
of `OpenObject`_ and `Django`_. Let's see how it goes...

.. _Werkzeug: http://werkzeug.pocoo.org/
.. _Jinja2: http://jinja.pocoo.org/2/
.. _Babel: http://babel.edgewall.org/
.. _pytz: http://pytz.sourceforge.net/
.. _Python: http://python.org/
.. _Django: http://djangoproject.org/
.. _OpenObject: https://launchpad.net/openobject/


Intentions & Goals
------------------

The primary intention of this project is to implement a web framework to make
it easy to develop highly modular web applications.

Another major goal is to implement a :ref:`database abstraction layer <dal>` which
can be used with any kind of database systems, be it an RDBMS or NoSQL database.

Following goals have been set:

* Database Abstraction Layer
    - Support for PostgreSQL
    - Support for MySQL
    - Support for SQLite3
    - Support for BigTable (google appengine datastore)
    - Support for OpenERP (via xmlrpc)
* Internationalization and localization support
* Command line tools for project management
* Complete documentation
* Extensive unit testing
* Packages (modular design)
    - Per package settings file
    - Support for extending an existing package with addon packages
    - Resources provided by addon package should get preference over
      original package
* Widget framework
    - Form generation and validation
    - Generic view generation (non-form widgets)
    - Declarative view definitions for data models
* Admin interface
    - activate/deactivate packages
    - configuration

