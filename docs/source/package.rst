Packages
========

A KalaPy project is a collection of several packages. A package represents
either a web application (e.g. a wiki or a blog) or an addon package. The
resources provided by an addon package will be served as resources of the
original package. This way, you can build a highly modular web applications
quickly.

Application Package
-------------------

For example, the included example project provides two packages. The `wiki`
package provides a simple wiki application and the `wiki_extended` package
provides extended features.

See how the original wiki application looks like:

.. image:: _static/wiki.png
    :width: 70%
    :scale: 100%
    :align: center

Addon Package
-------------

Now suppose, you want to change the behaviour, look and feel or even want to
provide new functionality to the wiki application, generally you have to edit
the wiki application. But what if for some reason, you don't wont to modify the
original application? Then generally, you should have to implement some kind of
addons system for your application.

KalaPy has built-in addons functionality, which let you create an addon package
similar to normal application package. In order to create an addon package, you
just have to specific the name of the package to be extended in the
:ref:`package settings <package-settings>`::

    EXTENDS = "wiki"

The included `wiki_extended` package extends the `wiki` application without
touching it. See how the wiki application looks like after activating
`wiki_extended` package:

.. image:: _static/wiki-extended.png
    :width: 70%
    :scale: 100%
    :align: center

You can see that the layout and look and feel is changed. Also note the search
feature has been implemented.

The resources including static contents, templates, models and view functions of
the `wiki_extended` package will be served as resources of the original `wiki`
package.
