.. currentmodule:: kalapy.db

Database Abstraction Layer
==========================

*KalaPy* provide a Database Abstraction Layer (DAL), an API that maps Python
objects to database objects. The API is designed such that it can work with
any kind of database management system, be it an RDBMS or NoSQL databases.
Currently, it supports SQLite3, PostgreSQL, MySQL and Google App Engine (GAE).

A programming model should be declared as a subclass of :class:`Model`,
declaring properties as any of :class:`Field` subclass. So if you want to
publish an article with title, text, and publishing date, you would do it
like this::

    from kalapy import db

    class Article(db.Model):
        title = db.String(size=100, required=True)
        pubdate = db.DateTime(default_now=True)
        text = db.Text(required=True)

You can then create new Article, like this::

    article = Article(title='My Article')
    article.text = "some text"
    article.save()
    db.commit()

You can query your articles using query interface provided, like::

    articles = Article.all().filter('pubdate >=', somedate) \
                            .order('-pubdate')
    for article in articles:
        print article.title

The input will be validated according to the properties to which it is being
assigned. That is, a :class:`DateTime` property can only be assigned a valid
``datetime`` value (real python :class:`~datetime.datetime`, or string
representation of ``datetime``).  Beside that you can also validate input by
providing a validator function while defining a field with `validator` argument
or by defining a method in the model class with ``validate_`` as prefix.

For example::

    def check_terms(value):
        if 'some_dirty_word' in value:
            raise db.ValidationError("doesn't follow the terms and conditions")

    class Article(db.Model):
        title = db.String(size=100, required=True)
        pubdate = db.DateTime(default_now=True)
        text = db.Text(required=True, validator=check_terms)

        def validate_title(self, value):
            if len(value) < 5:
                raise db.ValidationError('Title too short...')


The ``check_terms`` function is associated as a validator for ``text`` field
while the ``validate_title`` method is explicitly associated with ``title``
field as validator.

You can also relate models using any of the provided reference fields to
represent `many-to-one`, `one-to-one`, `one-to-many` or `many-to-many`
relationships among them. For example::

    class Comment(db.Model):
        title = db.String(size=100, required=True)
        text = db.Text()
        article = db.ManyToOne(Article)

A reverse lookup field named ``comment_set`` will be automatically created
in the ``Article`` model. Reference properties can be accessed like this::

    comment = Comment.get(key)
    print comment.article.title

    article = Article.get(key)
    for comment in article.comment_set.all().fetch(-1):
        print comment.title

The model class has a special readonly field named ``key`` that defines
*primary key* of your data model. The datatype of `key` value depends on
the underlying database engine. For RDBMS, it is generally an integer but
for GAE it is a string value.

Model
-----

.. autoclass:: Model
    :members:

.. autofunction:: get_model

.. autofunction:: get_models


Fields
------

.. autoclass:: FieldError
    :members:

.. autoclass:: ValidationError
    :members:

.. autoclass:: Field
    :members:

.. autoclass:: String
    :members:

.. autoclass:: Text
    :members:

.. autoclass:: Integer
    :members:

.. autoclass:: Float
    :members:

.. autoclass:: Decimal
    :members:

.. autoclass:: Boolean
    :members:

.. autoclass:: Date
    :members:

.. autoclass:: Time
    :members:

.. autoclass:: DateTime
    :members:

.. autoclass:: Binary
    :members:


Relational Fields
-----------------

.. autoclass:: ManyToOne
    :members:

.. autoclass:: OneToOne
    :members:

.. autoclass:: OneToMany
    :members:

.. autoclass:: ManyToMany
    :members:

Query
-----

Once you have your models, you need a way to retrieve stored model instances
from the database. As the DAL is designed to be DBMS independent it is quite
difficult to use SQL for this purpose. To deal with this issue, DAL provides
a generic query interface which is more pythonic. It also guards you from some
common vulnerabilities like SQL injection.

A :class:`Query` instance queries over instances of :class:`Model`.

You can create a :class:`Query` instance with a model class like this::

    users = Query(User).filter('name =', 'some%') \
                       .order('-name') \
                       .fetch(10)

This is equivalent to:

.. sourcecode:: sql

    SELECT * FROM 'user' WHERE 'name' LIKE 'some%' ORDER BY 'name' DESC LIMIT 10

The query string accepted by filter method is constructed by two components where
the LHS is a name of a field in the give model and RHS is an operator.

The query string supports following operators:

    ============= ==============================
    Operator      Meaning
    ============= ==============================
    `=`           like match
    `==`          exact match
    `>`           greater then
    `<`           less then
    `>=`          greater then or equal to
    `<=`          less then or equal to
    `!=`          not equal to
    `in`          within the given items
    `not in`      not within the give items
    ============= ==============================

For convenience, all of the filtering and ordering methods return "self", so
you can chain method calls like this:

.. sourcecode:: python

    users = Query(User).filter('name =', 'some%') \
                       .filter('age >=', 18) \
                       .filter('lang in', ['en', 'hi', 'gu']) \
                       .order('-age').fetch(100)

This is equivalent to:

.. sourcecode:: sql

    SELECT * FROM 'user' WHERE
        'name' LIKE 'some%' AND 'age' >= 18 AND 'lang' IN ('en', 'hi', 'gu')
    ORDER BY 'country' DESC LIMIT 100

You can see that multiple ``filter`` call results an ``ANDed`` expression. You
can generate ``ORed`` result using :class:`Q` like this:

.. sourcecode:: python

    from kalapy.db import Query, Q

    users = Query(User).filter(
        Q('name =', 'some%')|Q('lang in', ['en', 'hi', 'gu']))

This is equivalent to:

.. sourcecode:: sql

    SELECT * FROM 'user' WHERE
        'name' LIKE 'some%' OR 'lang' IN ('en', 'hi', 'gu')


This way you can build a complex query with ``AND`` and ``OR`` expressions.
However, the API doesn't support ``JOIN`` of multiple data models.

Proceed with the :class:`Query` documentation for more details...

.. autoclass:: Q
    :members:

.. autoclass:: Query
    :members:
