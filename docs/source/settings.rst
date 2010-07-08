Settings
========

A settings file contains all the configuration of your KalaPy application. A
settings file is just a normal Python module with module-level variables. The
settings module is located in the top-level project directory.

Available Settings
------------------

Here is the list of available settings.


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

INSTALLED_PACKAGES
++++++++++++++++++

Default::

    INSTALLED_PACKAGES = (
        'kalapy.contrib.sessions',
    )

List of installed packages.

PACKAGE_OPTIONS
+++++++++++++++

Default::

    PACKAGE_OPTIONS = {
        'wiki': {'submount': '/wiki'},
        'blog': {'submount': '/blog'},
    }

Package options (submount etc).


.. warning::

    As settings file may contain sensitive information like database password, you
    should limit access to it. For example, change file permission etc.

