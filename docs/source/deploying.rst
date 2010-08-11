Deployment Options
==================

Generally you run the built in server during development, but you should consider
other ways of running `KalaPy` applications when in production mode.

Apache (mod_wsgi)
-----------------

If you are using `Apache`_, you should consider using `mod_wsgi`_. See mod_wsgi
`installation instructions`_ for more information.

To run your application, you are required a python script. This file will contain
code `mod_wsgi` is executing on startup to get the ``application`` instance.

Here is one example script for `KalaPy` application::

    import os, sys

    PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
    PROJECT_LIB = os.path.join(PROJECT_DIR, 'lib')

    sys.path = [PROJECT_DIR, PROJECT_LIB] + sys.path

    from kalapy.web import Application
    from kalapy.admin import setup_environment

    import settings
    setup_environment(settings)

    application =  Application()

The next step is to create a configuration for your Apache server. Here is an
example configuration:

.. sourcecode:: apache

    <VirtualHost *>

        ServerName example.com

        WSGIDaemonProcess yourapp processes=1 threads=15 display-name=%{GROUP}
        WSGIProcessGroup yourapp

        WSGIScriptAlias / /var/www/yourapp/yourapp.wsgi

        <Directory /var/www/yourapp>
            Order deny,allow
            Allow from all
        </Directory>

    </VirtualHost>

See `mod_wsgi wiki`_ for more information.

.. _Apache: http://httpd.apache.com/
.. _mod_wsgi: http://code.google.com/p/modwsgi/
.. _installation instructions: http://code.google.com/p/modwsgi/wiki/QuickInstallationGuide
.. _mod_wsgi wiki: http://code.google.com/p/modwsgi/wiki/


Google App Engine
-----------------

See the :doc:`gae` guide for more information.

CGI
---

todo

FastCGI
-------

todo

Tornado
-------

todo
