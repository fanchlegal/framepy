Settings
========

A settings file contains all the configuration of your KalaPy application. A
settings file is just a normal Python module with module-level variables.

There are two kind of settings file, `project settings` located in the top-level
project directory and `package settings` located in the package directory.


.. _project-settings:

Project Settings
----------------

Here is the list of available project settings.


DATABASE_ENGINE
+++++++++++++++

Default::

    DATABASE_ENGINE = "sqlite3"

The database backend engine. Possible value can be either "sqlite3",
"postgresql", "mysql" or "gae".


DATABASE_NAME
+++++++++++++

Default::

    DATABASE_NAME = ""

The name of the database. For sqlite3, use full path to the sqlite3 database file.

DATABASE_USER
+++++++++++++

Default::

    DATABASE_USER = ""

The database username (must have rights to create database tables). Keep empty
for sqlite3 and gae.

DATABASE_PASSWORD
+++++++++++++++++

Default::

    DATABASE_PASSWORD = ""

The database password. Keep empty for sqlite3 and gae.

DATABASE_HOST
+++++++++++++

Default::

    DATABASE_HOST = ""

The database host. Keep empty for sqlite3 and gae.

DATABASE_PORT
+++++++++++++

Default::

    DATABASE_PORT = ""

The database port. Keep empty for sqlite3 and gae.

DATABASE_OPTIONS
++++++++++++++++

Default::

    DATABASE_OPTIONS = {}

Database specific options.

USE_I18N
++++++++

Default::

    USE_I18N = True

Enable/Disable internationalization support.

DEFAULT_LOCALE
++++++++++++++

Default::

    DEFAULT_LOCALE = "en_US"

Default locale to be used for internationalization and localization.

DEFAULT_TIMEZONE
++++++++++++++++

Default::

    DEFAULT_TIMEZONE = "UTC"

Default timezone, UTC recommended.

MIDDLEWARE_CLASSES
++++++++++++++++++

Default::

    MIDDLEWARE_CLASSES = (
        'kalapy.contrib.sessions.SessionMiddleware',
    )

List of Middleware classes.

SESSION_ENGINE
++++++++++++++

Default::

    SESSION_ENGINE = "memory"

Session storage engine (memory, memcached or database).

SESSION_OPTIONS
+++++++++++++++

Default::

    SESSION_OPTIONS = {
        'memcached_servers': [],
    }

Session related options. For example ``memcached_servers``. For memcached
engine, provide list of memcached servers. If DATABASE_ENGINE is set to
'gae' this option will be ignored.

SESSION_COOKIE
++++++++++++++

Default::

    SESSION_COOKIE = {
        'name': 'session_id',
        'age': 60 * 60 * 24 * 7 * 2,
        'domain': None,
        'path': '/'
    }

Session cookie options.

LOGGING
+++++++

Default::

    LOGGING = {
        'level': 'DEBUG',
        'format': '[%(asctime)s] %(levelname)s:%(name)s:%(message)s',
        'logfile': None,
    }

Settings for logging. The ``level`` can be one of ``'INFO'``, ``'DEBUG'`` or
``'ERROR'``. If ``logfile`` is not provided, `stderr` will be assumed.


STATIC_LINKS
++++++++++++

Default::

    STATIC_LINKS = {
        '/favicon.ico': 'static/favicon.ico',
        '/robots.txt': 'static/robots.txt',
    }

Override the static links. Useful to provide favicon.ico or robots.txt. You can
also provide static directory links to override original static dirs. Paths should
be absolute path or relative to the project directory. For example::

    STATIC_LINKS = {
        '/static': '/path/to/alternative/static/dir',
        '/favicon.ico': 'static/favicon.ico',
        '/foo/static': ('/path/to/foo/static1', '/path/to/foo/static2'),
    }

If you want to specify fallback directories, list them in tuple.

INSTALLED_PACKAGES
++++++++++++++++++

Default::

    INSTALLED_PACKAGES = (
        'kalapy.contrib.sessions',
    )

List of installed packages.

.. _package-settings:

Package Settings
----------------

Here is the list of available package settings.

NAME
++++

Default::

    NAME = "package_name"

The name of the package.

DESCRIPTION
+++++++++++

Default::

    DESCRIPTION = """
    """

Package description.

VERSION
+++++++

Default::

    VERSION = "1.0"

Package version string.

EXTENDS
+++++++

Default::

    EXTENDS = None

The name of the package that is extended by this package. In that case this
package is considered an addon package and resources provided by this package
will be served as the resources of extending package.

DEPENDS
+++++++

Default::

    DEPENDS = None

List of other packages this package depends on.

SUBMOUNT
++++++++

Default::

    SUBMOUNT = None

Submount to be used to mount this package. For example, ``'/wiki'``, ``'/blog'``
etc. Ignored for addon packages.

.. warning::

    As project settings file may contain sensitive information like database
    password, you should limit access to it. For example, change file permission
    etc.
