from kalapy import db

from foo.models import Foo

class Foo(Foo):
    msg = db.String(size=100)

class Fox(db.Model):
    name = db.String()
