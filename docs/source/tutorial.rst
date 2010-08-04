Tutorial
========

This tutorial will help you quickly getting started with *KalaPy*. This assumes
you already have *KalaPy* installed, if not please check the :doc:`installation`
section.

.. note::

    This tutorial is a work in progress and does not cover all the features. It
    is continuously being updated as *KalaPy* evolves.

Step 1: Create a Project
------------------------

A *KalaPy* project is a collection of a configuration module, an admin script and
several application packages. The :ref:`configuration module <project-settings>`
is a collection of settings like database settings etc. *KalaPy* provides a quickstart
script to generate initial set of files for your project.

From the command line, go to the directory where you would like to create your
project and run the following command::

    $ kalapy-quickstart.py Hello

A new project directory ``Hello`` will be created with the following directory
structure::

    Hello/
        admin.py
        settings.py
        static/
            robots.txt
            favicon.ico

These files are:

* ``admin.py`` - a command-line utility to perform various administrative tasks
* ``settings.py`` - the settings module hold project wide configuration settings
* ``static/robots.txt`` - web crawlers and robots exclusion settings
* ``static/favicon.ico`` - the favicon for your site (replace it with your own)

Step 2: Create a Package
------------------------

Now that your project is ready, you are set to start work.

A package represents either a web application (e.g. a wiki or a blog) or an addon
package that extends any existing application package and follows certain conventions.
*KalaPy* provides an admin utility that automatically generates initial directory
structure for your package.

To create your package, make sure you are in the ``Hello`` directory and type
following command::

    $ ./admin.py package blog

A new application package ``blog`` will be created under the current project
directory with following contents::

    blog/
        __init__.py
        models.py
        views.py
        settings.py
        tests.py
        static/
        templates/

The files here are:

* The ``settings.py`` can be used to defined package specific configuration settings.
  See :ref:`package-settings` for more information.
* The ``models.py`` is where you should define you models.
* The ``views.py`` is where you should define you view functions.
* The ``tests.py`` is where you should write tests.
* The ``static`` directory can be used to serve static contents.
* The ``templates`` directory should hold all the templates for the views.

The application package created here needs to be activated from the ``settings``
module of the project created earlier. Open the ``settings.py`` file and append
``blog`` to the list of ``INSTALLED_PACKAGES``.


.. note::

    A package can be extended by addon packages. Resources provided by those
    addon packages will be available as resources of the original package.


Step 3: Define the Models
-------------------------

If your application requires database support to store information, next step
is to define your data models. KalaPy provides it's own :doc:`api/db` to create
the data models.

Here with our ``blog`` application, we need to store some informations like
`articles`, `comments` made on them etc. The models should be defined under
``models.py`` like this::

    from kalapy import db

    class Article(db.Model):
        title = db.String(size=100, required=True)
        pubdate = db.DateTime(default_now=True)
        text = db.Text(required=True)

        def validate_title(self, value):
            if len(value) < 5:
                raise db.ValidationError('Title too short...')


    class Comment(db.Model):
        title = db.String(size=100, required=True)
        text = db.Text()
        article = db.ManyToOne(Article)

Step 4: Database Setup
----------------------

As you have defined your models, it's time to setup database to store the model
data. You should configure the database engine from the :ref:`project settings <project-settings>`
via following settings:

.. sourcecode:: python

    DATABASE_ENGINE = "sqlite3"

    DATABASE_NAME = "test_hello.db"

KalaPy supports ``sqlite3``, ``postgresql``, ``mysql`` and ``gae`` backend engines.
For simplicity, let we use ``sqlite3`` for this demo project.

Now as you have configured you database setup, next step is to create database
and required tables for the defined models.

First create the database file::

    $ touch test_hello.db

Then create tables::

    $ ./admin.py database sync

If you want to see the table schema, issue this command::

    $ ./admin.py database info blog

This will print the ``CREATE TABLE`` statements of all the modules defined in the
``blog`` package like this:

.. sourcecode:: sql

    CREATE TABLE "blog_article" (
        "key" INTEGER PRIMARY KEY AUTOINCREMENT,
        "title" VARCHAR(100) NOT NULL,
        "pubdate" DATETIME,
        "text" TEXT NOT NULL
    );
    CREATE TABLE "blog_comment" (
        "key" INTEGER PRIMARY KEY AUTOINCREMENT,
        "title" VARCHAR(100) NOT NULL,
        "text" TEXT,
        "article" INTEGER,
        FOREIGN KEY ("article") REFERENCES "blog_article" ("key")
    );

The output varies depending on the database backend you have selected. Use ``help``
to see more information on other available commands.

Step 5: Playing with the API
----------------------------

The ``admin.py`` script provides two commands to play with the *KalaPy* API.

Start an interactive python shell::

    $ ./admin.py shell

or, run an arbitrary python script in the context of current project::

    $ ./admin.py script somescript.py

Let's check with shell::

    >>> from kalapy import db
    >>> from blog.models import *
    >>> article = Article(title='my first article')
    >>> article.text = """
    ... some article
    ... text...
    ... """
    >>> article.save()
    >>> db.commit()
    >>> articles = Article.all().fetch(10)
    >>> for article in articles:
    ...     print article.title


Step 6: Define the Views
------------------------

Your application may have several views. A view can be an html page or json/xml
data that provides details about some specific information.

A KalaPy application generally serves views via view functions with or without
templates. For example, here with our blog application, we might have following
views:

* Home Page - displays few latest blog articles
* Article Page - displays a single article
* Comment Post - provides entry form to submit comments

and so on...

You should define your view functions inside the ``views.py`` module like::

    from kalapy import web
    from kalapy.web import request

    @web.route('/')
    def index():
        return """
        <h1>Hello World!</h1>
        """

    @web.route('/blog/<msg>')
    def blog(msg):
        return "Say: %s" % msg

The urls for the views should be defined using the :func:`~kalapy.web.route`
decorator. For for information see :doc:`web api documentation <api/web>`.

Step 7: Start the Development Server
------------------------------------

As you have defined your views, it's time to see it in action. *KalaPy* provides
a simple server for development purpose which can be launched using the admin
script like::

    $ ./admin.py runserver

You should see some logging information on your terminal, something similar to::

    [2010-08-04 19:55:30,965] INFO:pool: * Loading package: kalapy.contrib.sessions
    [2010-08-04 19:55:30,969] INFO:pool: * Loading module: kalapy.contrib.sessions.models
    [2010-08-04 19:55:30,971] INFO:pool: * Loading package: blog
    [2010-08-04 19:55:30,973] INFO:pool: * Loading module: blog.models
    [2010-08-04 19:55:30,974] INFO:pool: * Loading module: blog.views
    [2010-08-04 19:55:31,143] INFO:werkzeug: * Running on http://127.0.0.1:8080/
    ...
    ...

Launch you web browser and go to `http://127.0.0.1:8080/ <http://127.0.0.1:8080/>`_,
you should see your hello world greetings.
