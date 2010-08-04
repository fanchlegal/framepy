# -*- coding: utf-8 -*-
from __future__ import with_statement

from kalapy import db
from kalapy import web
from kalapy.conf import settings
from kalapy.test import TestCase

try:
    import simplejson as json
except:
    import json


class CoreTest(TestCase):

    def test_request_dispatching(self):
        c = self.client
        rv = c.get('/')
        assert rv.data == 'GET'
        rv = c.post('/')
        assert rv.status_code == 405
        assert sorted(rv.allow) == ['GET', 'HEAD']
        rv = c.head('/')
        assert rv.status_code == 200
        assert not rv.data  # head truncates
        assert c.get('/more').data == 'GET:100'
        rv = c.post('/more')
        assert rv.status_code == 405
        assert sorted(rv.allow) == ['GET', 'HEAD']
        assert c.get('/more/200').data == 'GET:200'
        assert c.post('/more/200').data == 'POST:200'
        rv = c.delete('/more/200')
        assert rv.status_code == 405
        assert sorted(rv.allow) == ['GET', 'HEAD', 'POST']

    def test_response_creation(self):
        c = self.client
        assert c.get('/response/unicode').data == u'Hällo Wörld'.encode('utf-8')
        assert c.get('/response/str').data == u'Hällo Wörld'.encode('utf-8')
        rv = c.get('/response/tuple')
        assert rv.data == 'Meh'
        assert rv.headers['X-Foo'] == 'Testing'
        assert rv.status_code == 400
        assert rv.mimetype == 'text/plain'
        rv = c.get('/response/dict')
        try:
            rv = c.get('/response/None')
        except ValueError, e:
            str(e) == 'View function should return a response'
            pass
        else:
            assert 'Expected ValueError'

    def test_url_generation(self):
        with self.request_context():
            assert web.url_for('response', kind="no thing", extra='test x') \
                == '/response/no%20thing?extra=test+x'
            assert web.url_for('response', kind="no thing", extra='test x', _external=True) \
                == 'http://localhost/response/no%20thing?extra=test+x'

        with self.request_context():
            assert web.url_for('bar:urls.index') == '/bar/'
            assert web.url_for('bar:urls.bar') == '/bar/bar'

        with self.request_context(path='/bar/'):
            assert web.url_for('urls.bar') == '/bar/bar'
            assert web.url_for('.bar') == '/bar/bar'

    def test_static_files(self):
        with self.request_context():
            static_file = web.url_for('static', filename='index.html')
            assert static_file == '/core/static/index.html'
            rv = self.client.get(static_file)
            assert rv.status_code == 200
            assert rv.data.strip() == '<h1>Hello World!</h1>'
            rv = self.client.get('/favicon.ico')
            assert rv.status_code == 200
            rv = self.client.get('/robots.txt')
            assert rv.status_code == 200


class JSONTest(TestCase):

    def test_jsonify(self):
        rv = self.client.get('/json1')
        assert rv.mimetype == 'application/json'
        json.loads(rv.data) == dict(a=1, b=2, c=[3, 4, 5])
        rv = self.client.get('/json2')
        assert rv.mimetype == 'application/json'
        json.loads(rv.data) == dict(a=1, b=2, c=[3, 4, 5])


class TemplateTest(TestCase):

    def test_template(self):
        rv = self.client.get('/template/1/2/3/4')
        assert rv.data == '<p>1/2/3/4</p>'


class MiddlewareTest(TestCase):

    def test_process_request(self):
        rv = self.client.get('/middleware/request')
        assert rv.data == 'process_request'
        rv = self.client.get('/middleware/response')
        assert rv.data == 'process_response'
        rv = self.client.get('/middleware/exception')
        assert rv.data == 'process_exception'


class PackageTest(TestCase):

    def test_package_resolution(self):
        assert self.client.get('/bar/bar').data == \
"""/bar/bar/static/foo.js
/foo/foo/static/bar.js
/bar/bar
/foo/foo"""

    def test_extends_template(self):
        assert self.client.get('/foo/foo').data == \
"""/foo/foo/static/foo.js
/bar/bar/static/bar.js
/foo/foo
/bar/bar
/foo/fox
/foo/fox"""

    def test_extends_static(self):
        rv = self.client.get('/foo/foo/static/foo.js').data
        self.assertEqual(rv, "var FOO = 'fox'\n")

    def test_extends_models(self):
        m = db.get_model('foo:foo')
        self.assertEqual(m.__module__, "foo_extended.models")
        self.assertEqual(m._meta.package, "foo")
        m = db.get_model('foo:fox')
        self.assertEqual(m.__module__, "foo_extended.models")
        self.assertEqual(m._meta.package, "foo")

    def test_extends_views(self):
        with self.request_context():
            self.assertEqual(web.url_for('foo:fox'), "/foo/fox")

        with self.request_context('/foo/fox'):
            self.assertEqual(web.url_for('foox'), '/foo/foox')
            self.assertEqual(web.url_for('.fox'), '/foo/fox')
            self.assertEqual(web.url_for('foo:foo'), '/foo/foo')
            self.assertEqual(web.url_for('foo'), '/foo/foo')
