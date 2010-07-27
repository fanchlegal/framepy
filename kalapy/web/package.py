# -*- coding: utf-8 -*-
"""
kalapy.web.package
~~~~~~~~~~~~~~~~~~

Implements :class:`Package` that represent a package.

:copyright: (c) 2010 Amit Mendapara.
:license: BSD, see LICENSE for more details.
"""
import os, sys

from jinja2 import FileSystemLoader
from werkzeug.routing import Rule, Map

from kalapy.conf import Settings, settings, package_settings


__all__ = ('Package',)


class PackageType(type):
    """A meta class to ensure only one instance of :class:`Package` exists
    for a given package name.
    """

    #: cache of all the Package instances
    ALL = {}

    def __call__(cls, *args):
        name = args[0] if args else None
        if name not in cls.ALL:
            cls.ALL[name] = super(PackageType, cls).__call__(*args)
        return cls.ALL[name]

    def from_view(cls, view_func):
        """A factory method to create package instance from the view function.
        """
        module = view_func.__module__
        name = module[:module.find('.views')].rsplit('.', 1)[-1]
        return cls(name)


class Package(object):
    """Container object that represents an installed package.

    A package can be enabled/disabled from `settings.INSTALLED_PACKAGES`. This
    class is intended for internal use only.

    For more information on packages, see...

    :param name: name of the package
    :param path: directory path where package is located
    """
    __metaclass__ = PackageType

    #: :class:`werkzeug.routing.Map` instance, shared among all the Packages
    urls = Map()

    #: view functions, shared among all the packages
    views = {}

    #: Package settings
    settings = None

    def __init__(self, name, path=None):

        if path is None:
            path = os.path.abspath(os.path.dirname(sys.modules[name].__file__))

        self.name = name
        self.path = path

        options = dict(NAME=self.name)
        try:
            execfile(os.path.join(self.path, 'settings.py'), {}, options)
        except IOError:
            pass
        self.settings = Settings(package_settings, **options)

        self.submount = self.settings.SUBMOUNT

        # static dir info
        self.static = os.path.join(self.path, 'static')
        if not os.path.isdir(self.static):
            self.static = None

        # add rule for static urls
        if self.static:
            prefix = '/static' if self.is_main else '/%s/static' % name
            self.add_rule('%s/<filename>' % prefix, 'static', build_only=True)
            prefix = '%s%s' % (self.submount or '', prefix)
            self.static = (prefix, self.static)

        # create template loader
        self.jinja_loader = FileSystemLoader(self.get_resource_path('templates'))

    @property
    def is_main(self):
        """Whether this is the main package (the project package)
        """
        return self.name == settings.PROJECT_NAME

    def get_resource_path(self, name):
        """Get the absolute path the the given resource.

        :param name: path to the resource relative to this package
        """
        return os.path.join(self.path, name)

    def get_resource_stream(self, name):
        """Returns file stream object of the given resource.

        :param name: path to the resource relative to this package
        """
        return open(self.get_resource_path(name), 'rb')

    def add_rule(self, rule, endpoint, func=None, **options):
        """Add URL rule with the specified rule string, endpoint, view
        function and options.

        Function must be provided if endpoint is None. In that case endpoint
        will be automatically generated from the function name. Also, the
        endpoint will be prefixed with current package name.

        Other options are similar to :class:`werkzeug.routing.Rule` constructor.
        """
        if endpoint is None:
            assert func is not None, 'expected view function if endpoint' \
                    ' is not provided'

        if endpoint is None:
            endpoint = '%s.%s' % (func.__module__, func.__name__)
            __, endpoint = endpoint.rsplit('views.', 1)

        if not self.is_main:
            endpoint = '%s.%s' % (self.name, endpoint)

        options.setdefault('methods', ('GET',))
        options['endpoint'] = endpoint

        if self.submount:
            rule = '%s%s' % (self.submount, rule)

        self.urls.add(Rule(rule, **options))
        self.views[endpoint] = func

    def route(self, rule, **options):
        """Same as :func:`route`
        """
        def wrapper(func):
            self.add_rule(rule, None, func, **options)
            return func
        return wrapper
