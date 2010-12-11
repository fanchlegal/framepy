#: Name of the package.
NAME = "wiki_extended"

#: Package description.
DESCRIPTION = """
An example addon package to extend the wiki package. The resources provided
by this package will be available as resources of the wiki package.
"""

#: Package version string.
VERSION = "1.0"

#: Name of the package that is extended by this package.
#: In that case this package is considered an addon package
#: and resources provided by this package will be served as
#: the resources of extending package.
EXTENDS = 'wiki'

#: Other packages this package depends on.
DEPENDS = None
