Installation
============

This guide with help you to properly install *KalaPy* and all it's dependencies.


.. note::

    This is an initial version of installation guide and doesn't provide much
    information on some topics, but will be improved as it goes...


Prerequisite
------------

* Python >= 2.5
* Werkzeug >= 0.6.2
* Jinja2 >= 2.4.1
* simplejson >= 2.1.1 (not required for py2.6)
* Pygments >= 1.3.1 (optional, to see colourful output on terminal)
* MySQLdb >= 1.2.1 (optional, if you want to use MySQL backend engine)
* psycopg2 >= 2.2.1 (optional, if you want to use PostgreSQL backend engine)

I assume you already have Python installed on you system.

virtualenv
----------

Follow this link more information on `virtualenv`_.

I assume you are using *ubuntu* (mine is ubuntu lucid with python 2.6).
Issue following commands if you haven't installed virtualenv package yet.

.. sourcecode:: text

    $ sudo apt-get install python-virtualenv

Now create your virtualenv directory, like:

.. sourcecode:: text

    $ virtualenv /path/to/your/env
    New python executable in env/bin/python
    Installing setuptools............done.

Now, you should activate it, whenever you work with it.

.. sourcecode:: text

    $ . env/bin/activate

Now you can just enter the following command to get KalaPy installed in
your virtualenv::

    $ easy_install KalaPy

After installed, type following command to see whether it is properly installed
or not:

.. sourcecode:: text

    $ kalapy-quickstart.py
    Usage: kalapy-quickstart.py <project>

    Create a KalaPy project with the given project name in the current directory.

    options:

      -v --verbose enable verbose output
      -h --help    display help and exit

.. _virtualenv: http://pypi.python.org/pypi/virtualenv/

System Wide Installation
------------------------

This is not recommended, as KalaPy is still unstable, under heavy development
and not tested well.

.. sourcecode:: text

    $ sudo easy_install KalaPy


Playing with the Source
-----------------------

*KalaPy* is an open source project released under BSD license. You can grab
the latest sources from `github.com <http://github.com/cristatus/KalaPy>`_.
