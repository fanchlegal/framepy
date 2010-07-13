# -*- coding: utf-8 -*-
"""
kalapy.web.wrappers
~~~~~~~~~~~~~~~~~~~

Implements :class:`Request` and :class:`Response`.

:copyright: (c) 2010 Amit Mendapara.
:license: BSD, see LICENSE for more details.
"""

from werkzeug import Request as BaseRequest, Response as BaseResponse

__all__ = ('Request', 'Response',)


class Request(BaseRequest):
    """The request object, remembers the matched endpoint, view arguments and
    current package.
    """

    @property
    def package(self):
        if self.endpoint:
            return self.endpoint.split('.', 1)[0]


class Response(BaseResponse):
    """The response object that is used by default, with default mimetype
    set to `'text/html'`.
    """
    default_mimetype = 'text/html'

