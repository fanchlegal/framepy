Deployment Options
==================

Generally you run the built in server during development, but you should
consider other ways of running `KalaPy` applications when in production
mode. KalaPy's one of the main goal is easy of deployment on variety of
platforms. There are several options to easily deploy `KalaPy` but we
would recommend you try :ref:`mod_wsgi <apache-mod-wsgi>` first, as in
most cases it will be the easiest and most stable deployment choice.

.. _apache-mod-wsgi:

Apache (mod_wsgi)
-----------------

If you are using `Apache`_, you should consider using `mod_wsgi`_. The
official `mod_wsgi documentation`_ is great source of information on how
to use `mod_wsgi`. You probably want to start with the `installation guide`_.

.. _Apache: http://httpd.apache.com/
.. _mod_wsgi: http://code.google.com/p/modwsgi/
.. _mod_wsgi documentation: http://code.google.com/p/modwsgi/wiki/
.. _installation guide: http://code.google.com/p/modwsgi/wiki/QuickInstallationGuide
.. _lighthttpd: http://www.lighttpd.net/
.. _Nginx: http://www.nginx.org/

The WSGI Script
+++++++++++++++

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

The Configuration
+++++++++++++++++

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


Serving Media files
+++++++++++++++++++

It is a common practice to serve static media contents via a separate
web server like `Nginx`_, `lighthttpd`_ or even a stripped down version
of `Apache`_.

KalaPy's :doc:`packaging system <package>` allows you to override static
contents provided by a package with addon packages. So you must be careful
of serving static contents via separate web server.

Generally, you should only serve media files like videos, documents, audio
files etc. through a separate web server and leave the css/javascript and
related images to be served by the application. However, there is nothing
that can prevent you to server all kind of static data via separate web
server but you must be aware of what you are doing else it will break the
packaging functionality of `KalaPy`.

Here is an example configuration for Apache:

.. sourcecode:: apache

    <VirtualHost *>

        ServerName example.com

        WSGIDaemonProcess yourapp processes=1 threads=15 display-name=%{GROUP}
        WSGIProcessGroup yourapp

        Alias /robots.txt /var/www/yourapp/static/robots.txt
        Alias /favicon.ico /var/www/yourapp/static/favicon.ico

        # your media contents
        Alias /media/ /var/www/yourapp/static/media/

        # the top-level static contents
        AliasMatch ^/static/(.*)$   /var/www/yourapp/static/$1

        # following settings will serve static contents provided by packages
        # however, you can leave package specific contents to be served by
        # KalaPy itself.

        # package static contents
        AliasMatch ^/blog/static/(.*)$ /var/www/yourapp/blog/static/$1

        # if you have a wiki application mounted on a subdir '/wiki' with
        # addons packages (kalapy example)
        AliasMatch ^/wiki/wiki/static/(.*)$ /var/www/yourapp/wiki_extended/static/$1
        AliasMatch ^/wiki/wiki/static/(.*)$ /var/www/yourapp/wiki/static/$1

        <Directory /var/www/yourapp/static>
            Order deny,allow
            Allow from all
        </Directory>

        WSGIScriptAlias / /var/www/yourapp/yourapp.wsgi

        <Directory /var/www/yourapp>
            Order deny,allow
            Allow from all
        </Directory>

    </VirtualHost>

However, as said before, if you are not sure then leave it to `KalaPy` to serve
the static contents provided by packages.

Google App Engine
-----------------

See the :doc:`gae` guide for more information.

Other Options
-------------

This section will describe other deployment options.

CGI
+++

todo

FastCGI
+++++++

todo

Tornado
+++++++

todo
