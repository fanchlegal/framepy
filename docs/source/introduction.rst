Introduction
================================================================================

*KalaPy* is a web application framework for `Python`_ providing it's own
:doc:`api/db`, web components based on `Werkzeug`_, templating using `Jinja2`_
template engine and full :doc:`i18n` support via `Babel`_ and `pytz`_ and much
more...

The development is still under alpha stage and API might change during this
period. I welcome your useful suggestions/thoughts about how to improve it and
how it should look like.

.. _Werkzeug: http://werkzeug.pocoo.org/
.. _Jinja2: http://jinja.pocoo.org/2/
.. _Babel: http://babel.edgewall.org/
.. _pytz: http://pytz.sourceforge.net/
.. _Python: http://python.org/
.. _OpenERP: https://launchpad.net/openobject/


The Intentions
--------------

The primary intention of this project is to implement a web framework to make
it easy to develop highly modular web applications.

Another major goal is to implement a :doc:`database abstraction layer <api/db>`
which can be used with any kind of database systems, be it an RDBMS or NoSQL
database.

The Goals
---------

Following goals have been set:

* Database Abstraction Layer
    - Support for PostgreSQL
    - Support for MySQL
    - Support for SQLite3
    - Support for BigTable (google appengine datastore)
    - Support for `OpenERP`_ (via xmlrpc)
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
