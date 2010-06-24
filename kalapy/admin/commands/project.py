"""
kalapy.admin.commands.project
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This module implements `startproject` and `startpackage` commands to
start a new project or an application package.

:copyright: (c) 2010 Amit Mendapara.
:license: BSD, see LINCESE for more details.
"""
import os, sys, re, shutil, string

from kalapy.admin import Command, ActionCommand, CommandError


def copy_template(template, target, context):

    source = os.path.dirname(os.path.dirname(__file__))
    source = os.path.join(source, template)

    names = os.listdir(source)

    if names and not os.path.exists(target):
        os.mkdir(target)

    for name in names:
        srcname = os.path.join(source, name)
        dstname = os.path.join(target, name)

        if os.path.isdir(srcname):
            continue

        if srcname.endswith('_t'):
            dstname = dstname[:-2]

        shutil.copy2(srcname, dstname)

        if srcname.endswith('_t'):
            content = open(srcname).read()
            content = string.Template(content).safe_substitute(context)

            fo = open(dstname, 'w')
            fo.write(content)
            fo.close()

def check_name(name):
    pat = re.compile('^[_a-zA-Z]\w*$')
    if not pat.search(name):
        raise CommandError("Invalid name '%s'" % name)

    try:
        __import__(name)
        raise CommandError('name conflicts with existing python module.')
    except ImportError:
        pass


class StartProject(Command):
    """start a new project
    """
    name = "startproject"
    usage = "%name <name>"

    scope = None

    def execute(self, options, args):
        try:
            name = args[0]
        except:
            self.print_help()

        check_name(name)

        if options.verbose:
            print "Creating %s..." % name
        copy_template('project_template', name, {'name': name, 'name_lower': name.lower()})


class StartApp(Command):
    """start a new package
    """
    name = "startpackage"
    usage = "%name <name>"

    def execute(self, options, args):
        try:
            name = args[0]
        except:
            self.print_help()

        check_name(name)
        if options.verbose:
            print "Creating %s..." % name
        copy_template('package_template', name, {'name': name})

        for d in ('static', 'templates',):
            os.mkdir('%s/%s' % (name, d))

class GAEProject(ActionCommand):
    """make this project google appengine compatible.
    """
    name = "gae"

    def action_app(self, options, args):
        """create appengine specific files (app.yaml, gaehandler.py).
        """
        from kalapy.conf import settings
        name = settings.PROJECT_NAME
        context = {'appname': name.lower(), 'name': name}
        if options.verbose:
            print "Creating app.yaml..."
        copy_template('gae_template', os.curdir, context)

    def action_libs(self, options, args):
        """install dependencies in lib dir.
        """
        from werkzeug import import_string
        libs = set(['kalapy', 'werkzeug', 'jinja2',
                    'babel', 'pytz', 'simplejson'] + args)

        if not os.path.exists("lib"):
            os.mkdir("lib")

        for lib in libs:
            mod = import_string(lib)
            src = mod.__file__
            if src.endswith('.pyc'):
                src = src[:-1]
            if src.endswith('__init__.py'):
                src = os.path.dirname(mod.__file__)
                dest = os.path.join("lib", lib)
                if not os.path.exists(dest):
                    if options.verbose:
                        print "Copying %s" % lib
                    shutil.copytree(src, dest)
            else:
                dest = os.path.join("lib", "%s" % os.path.basename(src))
                if os.path.exists(dest):
                    continue
                if options.verbose:
                    print "Copying %s" % os.path.basename(dest)
                shutil.copy2(src, dest)

        def do_clean(args, path, files):
            for f in files:
                f = os.path.join(path, f)
                __, x = os.path.splitext(f)
                if x in args:
                    os.remove(f)
        os.path.walk("lib", do_clean, ['.pyc', '.pyo', '.so'])


