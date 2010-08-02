# -*- coding: utf-8 -*-
"""
kalapy.web.local
~~~~~~~~~~~~~~~~

Defines context local objects.

:copyright: (c) 2010 Amit Mendapara.
:license: BSD, see LICENSE for more details.
"""
from werkzeug import LocalStack, LocalProxy


__all__ = ('request',)


class RequestContext(object):
    """The request context will be created at the begining of the request
    and removed at the end of a request.
    """
    def __init__(self, app, request):
        self.request = request

    def __enter__(self):
        _request_ctx_stack.push(self)
        return self

    def __exit__(self, exc_type, exc_value, tb):
        _request_ctx_stack.pop()


_request_ctx_stack = LocalStack()

#: The request context instance
_request_context = LocalProxy(lambda: _request_ctx_stack.top)

#: The request instance of the current request context
request = LocalProxy(lambda: _request_ctx_stack.top.request)
