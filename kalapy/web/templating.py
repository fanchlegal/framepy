# -*- coding: utf-8 -*-
"""
kalapy.web.templating
~~~~~~~~~~~~~~~~~~~~~

Implements templating support using Jinja2.

:copyright: (c) 2010 Amit Mendapara.
:license: BSD, see LICENSE for more details.
"""
from jinja2 import Environment

from kalapy.web.local import request


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
    """Render the template from the `templates` folder of the current package
    with the given context.

    If you want to refer to a template from another package, prefix the name
    with that package name like `package:template`. Also, if you wish to refer
    to a template from the global template dir just prefix it with `:`.

    Here are few examples:

    =============== ===================== ==============================
    Active Package  Template Name         Terget Template
    =============== ===================== ==============================
    `blog`          ``'index.html'``      '/blog/templates/index.html'
    `wiki`          ``'index.html'``      '/wiki/templates/index.html'
    `any`           ``'blog:index.html``  '/blog/templates/index.html'
    `any`           ``':index.html``      '/templates/index.html'
    =============== ===================== ==============================

    Same rule applies to the `extends` and `inculde` templates directives.

    .. note::

        If you refer a template from another package, all the `extends`,
        `include` and `import` statements will be resolved with current
        package's template loader if the template names are not prefixed
        appropriately. Same is true for `url_for` used within the referenced
        template

    :param template: the name of the template to be rendered.
    :param context: the variables that should be available in the context
                    of the template.

    :returns: string generated after rendering the template
    :raises: :class:`TemplateNotFound` or any other exceptions thrown during
             rendering process
    """
    if ':' not in template:
        template = '%s:%s' % (request.package, template)
    return request.current_app.jinja_env.get_template(template).render(context)
