# -*- coding: utf-8 -*-
"""
kalapy.web.templating
~~~~~~~~~~~~~~~~~~~~~

Implements templating support using Jinja2.

:copyright: (c) 2010 Amit Mendapara.
:license: BSD, see LICENSE for more details.
"""
from jinja2 import Environment

from kalapy.web.local import _request_context


__all__ = ('render_template',)


class JinjaEnvironment(Environment):
    """Custom Jinja environment, makes sure that template is correctly resolved.
    """
    def join_path(self, template, parent):
        if ':' not in template:
            package = parent.split(':',1)[0]
            return '%s:%s' % (package, template)
        return template


def render_template(template, **context):
    """Render the template of the current package with the given context.

    The template loader will try to load the template from the `templates`
    folder of the current package. If there are any addon packages activated
    for the current package, the loader will give prefences to the `templates`
    provided with the addon packages.

    :param template: the name of the template to be rendered.
    :param context: the variables that should be available in the context
                    of the template.

    :returns: string generated after rendering the template
    :raises: :class:`TemplateNotFound` or any other exceptions thrown during
             rendering process
    """
    ctx = _request_context
    template = '%s:%s' % (ctx.request.package, template)
    return ctx.current_app.jinja_env.get_template(template).render(context)
