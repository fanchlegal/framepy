Web Components
==============

This chapter will provide api documentation of the web components of the KalaPy
framework.

.. automodule:: kalapy.web
    :members:

Request
-------

.. autoclass:: Request
    :members:

Response
--------

.. autoclass:: Response
    :members:

Application
-----------

.. autoclass:: Application
    :members:

Middleware
----------

.. autoclass:: Middleware
    :members:

Package
-------

.. autoclass:: Package
    :members:

Routing
-------

.. autofunction:: route

.. autofunction:: url_for

.. autofunction:: redirect

.. autofunction:: locate

Templates
---------

.. automodule:: kalapy.web.templating
    :members:


.. currentmodule:: kalapy.web

Request Context
---------------

.. data:: request

    The request instance of the current request context.


Other Useful Functions & Classes
--------------------------------

.. autofunction:: jsonify

.. function:: json

    The standard :func:`simplejson.json` function exposed for convenience.

.. autofunction:: abort

.. autoclass:: HTTPException

.. autoclass:: NotFound

.. autoclass:: SecureCookie

    See :class:`~werkzeug.contrib.securecookie.SecureCookie` for more information.
