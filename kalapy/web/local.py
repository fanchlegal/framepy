# -*- coding: utf-8 -*-
"""
kalapy.web.local
~~~~~~~~~~~~~~~~

Defines context local objects.

:copyright: (c) 2010 Amit Mendapara.
:license: BSD, see LICENSE for more details.
"""
from werkzeug.local import Local, LocalManager


__all__ = ('request',)


# context local support
_local = Local()
_local_manager = LocalManager([_local])

# context local variable
request = _local('request')

