Admin Scripts
=============

The ``kalapy-quickstart.py`` is a command line script to create *KalaPy* projects.
The generated project skeleton includes an ``admin.py`` script that can be used
for administrative tasks for the project.

Available Scripts
-----------------

.. describe:: kalapy-quickstart.py <project>

The ``kalapy-quickstart.py`` script can be used to create new projects.

.. describe:: admin.py <command> [options] [args]

Run ``admin.py help`` to see list of available commands.
Run ``admin.py help command`` to see help of the given command, it's options
and command actions.

Available Commands
------------------

.. describe:: admin.py package <name>

The ``package`` command can be used to create new package skeleton.

.. describe:: admin.py database <action> [options]

The ``database`` command can be used to perform various database related tasks.

.. describe:: admin.py runserver [options]

The ``runserver`` command start a simple wsgi application server for development
environment.

.. describe:: admin.py shell [options] [args]

Runs a Python interactive interpreter in the context of current project.

.. describe:: admin.py script <FILE>

Similar to the ``shell`` command but runs an arbitrary script in the context
of current project.

.. describe:: admin.py babel <action> [options] [package [package [...]]]

Perform :doc:`i18n` message catalog actions.

.. describe:: admin.py test [name [name [name [...]]]]

Run the tests specified by the given names. A test name can be:

* ``package_name``
* ``package_name:test_fullname``

A ``test_fullname`` should be a fully qualified name relative to ``package.tests``
module. For example:


.. code-block:: text

    admin.py test foo
    admin.py test foo:FooTest
    admin.py test foo:FooTest.test_foo
    admin.py test bar:db_tests.DBTest
    admin.py test bar:db_tests.DBTest.test_mymodel
    admin.py test bar:view_tests.PaginationTest

If test names are not given run all the tests of the installed packages.

.. describe:: admin.py gae <action> [options] [args]

Perform :doc:`google appengine <gae>` specific tasks.
