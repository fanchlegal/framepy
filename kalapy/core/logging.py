from __future__ import absolute_import

import os
import sys
import logging
import logging.handlers

from kalapy.conf import settings


LOG_FORMAT = '[%(asctime)s] %(levelname)s:%(name)s:%(message)s'
LOG_LEVELS = {
    'INFO': logging.INFO,
    'DEBUG': logging.DEBUG,
    'ERROR': logging.ERROR,
}

def init_logger():
    """Initialize the logger. Do nothing for google app engine.
    """
    if settings.DATABASE_ENGINE == "gae":
        return

    level = settings.LOGGING.get('level') or 'INFO'
    format = settings.LOGGING.get('format') or LOG_FORMAT
    logfile = settings.LOGGING.get('logfile')

    level = logging.DEBUG if settings.DEBUG else LOG_LEVELS.get(level)
    logging.basicConfig(level=level, format=format)

    if logfile:
        try:
            handler = logging.handlers.TimedRotatingFileHandler(
                logfile, 'D', 1, 30)
        except Exception:
            sys.stderr.write('ERROR: unable to create log file: %s' % str(e))
        else:
            formatter = logging.Formatter(format)
            handler.setFormatter(formatter)
            # Get rid of all the handlers already attached to it.
            del logging.getLogger().handlers[:]
            logging.getLogger().addHandler(handler)
            logging.getLogger().setLevel(level)
