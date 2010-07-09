.. _gae:

Google App Engine
=================

*KalaPy* is fully compatible with `Google App Engine`_, including the
:ref:`dal`. Actually, the :ref:`dal` resembles GAE datastore API in some extents,
especially the :class:`db.Query <kalapy.db.Query>` interface.

However, following limitations have been imposed:

    * No read/write access to file system.
    * No transaction support.
    * You can not perform queries with multiple inequality filters.

.. Google App Engine: http://code.google.com/appengine/

Getting started
---------------

You must have access to the `Google App Engine`_ Python SDK on your system. Download
the SDK and extract the package somewhere and set an environment variable ``GAE_HOME``
pointing to the SDK directory. On Linux, do this:

.. sourcecode:: text

    export GAE_HOME=/path/to/google_appengine

KalaPy admin utility provides a ``gae`` command to perform various GAE related
tasks. Apply ``./admin.py gae -h`` command to see full help:

.. sourcecode:: text

    admin.py gae <action> [options] [args]

    Perform google appengine specific tasks.

    Use the 'appcfg.py' and 'dev_appserver.py' (included in appengine sdk)
    for other appengine specific tasks.

    options:

      -a --address hostname for the appserver
      -p --port    port number for the appserver
      -i --install install libs (extra libs as arguments)
      -v --verbose enable verbose output
      -h --help    display help and exit

    available actions:

      prepare    prepare this project for google appengine.
      rollback   launch 'appcfg.py rollback'
      runserver  launch 'dev_appserver.py runserver'
      update     launch 'appcfg.py update'

The first action you should perform is to prepare current project for GAE. This
can be done with ``prepare`` action. Issue following command.

.. sourcecode:: text

    ./admin.py gae prepare

This will create ``app.yaml`` and ``gae_handler.py`` scripts in the top-level
project directory.

Configuration
-------------

The ``DATABASE_ENGINE`` configuration should be changed to ``"gae"`` and if
you wish to use `session` change the ``SESSION_ENGINE`` to either ``"db"`` or
``"memcached"``::

    DATABASE_ENGINE = "gae"

    ...

    SESSION_ENGINE = "memcached"

Also, make sure that the ``application`` name is properly set in ``app.yaml``.

Run the development server
--------------------------

The ``gae`` admin command provides ``runserver`` action that will launch the
``dev_appserver`` that comes with the GAE SDK.

.. sourcecode:: text

    ./admin.py gae runserver

Deploy the Application
----------------------

Once your application is ready, you can deploy it on `appengine <http://appengine.google.com/>`_.
But before doing that, you have to prepare your application project to include
all the thirdparty Python packages including KalaPy itself.

The ``prepare`` action of the ``gae`` command with ``-i`` option can be used to
populate local `lib` directory with all the required Python packages. You can
also pass additional package names to the command line if you wish. For example,
here is the command used to prepare the KalaPy example application:

.. sourcecode:: text

    ./admin.py gae prepare -i docutils roman

As the example application depends on `docutils` and `roman` modules. The `KalaPy`
and other dependencies will be automatically installed in a local `lib` directory.

Now your application is ready to be deployed on GAE platform. Just issue following
command:

.. sourcecode:: text

    ./admin.py gae update

You will be prompted for your GAE username and password. Once deployed, you can
access your application from `http://your-app.appspot.com/`.

The included *KalaPy* example project has been deployed on GAE this way. You can
access it `here <http://kalapy-demo.appspot.com/>`_.

