# -*- coding: utf-8 -*-
"""
kalapy.web.package
~~~~~~~~~~~~~~~~~~

Implements :class:`Package` that represent a package.

:copyright: (c) 2010 Amit Mendapara.
:license: BSD, see LICENSE for more details.
"""
import os, sys

try:
    import threading
except ImportError:
    import dummy_threading as threading

from jinja2 import FileSystemLoader

from werkzeug import find_modules, import_string
from werkzeug.routing import Rule, Map

from kalapy.conf import Settings, settings, package_settings
from kalapy.utils.containers import OrderedDict


__all__ = ('Package',)


def get_package_name(module_name):
    """Return the package name from the given module name.

    This function takes care of ``rapido.contrib`` packages returning
    correct package name.

        >>> print get_package_name('hello.models')
        ... 'hello'
        >>> print get_package_name('hello.views.foo')
        ... 'hello'
        >>> print get_package_name('kalapy.contrib.sessions.models')
        ... 'sessions'
        >>> print get_package_name('hello')
        ... 'hello'

    :param module: a string, module name
    """
    if module_name.startswith('kalapy.contrib.'):
        module_name = module_name[15:]
    return module_name.split('.', 1)[0]


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

    def from_view_function(cls, func):
        """A factory method to create package instance from the view function.
        """
        return cls(get_package_name(func.__module__))


class Package(object):
    """Container object that represents an installed package.

    A package can be enabled/disabled from `settings.INSTALLED_PACKAGES`. This
    class is intended for internal use only.

    For more information on packages, see...

    :param name: name of the package
    :param path: directory path where package is located
    """
    __metaclass__ = PackageType

    #: list of :class:`werkzeug.routing.Rule` objects, defined by this package.
    rules = None

    #: view functions provided by this package.
    views = None

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
        self.rules = []
        self.views = {}

        # static dir info
        self.static = os.path.join(self.path, 'static')
        if not os.path.isdir(self.static):
            self.static = None

        # add rule for static urls
        if self.static:
            prefix = '/%s/static' % name
            self.add_rule('%s/<filename>' % prefix, 'static', build_only=True)
            prefix = '%s%s' % (self.submount or '', prefix)
            self.static = (prefix, self.static)

        # create template loader
        self.jinja_loader = FileSystemLoader(os.path.join(self.path, 'templates'))

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

        endpoint = '%s.%s' % (self.name, endpoint)

        options.setdefault('methods', ('GET',))
        options['endpoint'] = endpoint

        if self.submount:
            rule = '%s%s' % (self.submount, rule)

        self.rules.append(Rule(rule, **options))
        self.views[endpoint] = func

    def route(self, rule, **options):
        """Same as :func:`route`
        """
        def wrapper(func):
            self.add_rule(rule, None, func, **options)
            return func
        return wrapper


class PackageLoader(object):
    """Package loader automatically loads all the installed packages
    listed in ``settings.INSTALLED_PACKAGES``.
    """

    __shared_state = dict(
        packages = OrderedDict(),
        loaded = False,
        lock = threading.RLock(),
    )

    def __init__(self):
        self.__dict__ = self.__shared_state

    def load_modules(self, package, name):

        modules = tuple(find_modules(package, include_packages=True))
        fullname = '%s.%s' % (package, name)

        result = []

        if fullname in modules:
            mod = import_string(fullname)
            result.append(mod)

        try:
            submodules = tuple(find_modules(fullname))
        except (ValueError, AttributeError):
            return result

        for module in submodules:
            mod = import_string(module)
            result.append(mod)

        return result

    def load(self):
        """Load the installed packages.
        """
        if self.loaded:
            return

        self.lock.acquire()
        try:
            for package in settings.INSTALLED_PACKAGES:
                if package in self.packages:
                    continue

                if package not in sys.modules:
                    import_string(package)

                self.packages[package] = pkg = Package(package)

                self.load_modules(package, 'models')
                self.load_modules(package, 'views')

            self.loaded = True
        finally:
            self.lock.release()

loader = PackageLoader()
