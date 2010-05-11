from rapido.db.engines import database
from rapido.test import TestCase

from models import Article


class Internal(TestCase):

    def test_create_table(self):
        self.assertTrue(database.exists_table(Article._meta.table))

    def test_drop_table(self):
        database.drop_table(Article._meta.table)
        self.assertFalse(database.exists_table(Article._meta.table))
        database.rollback()

    def test_alter_table(self):
        database.alter_table(Article)
        database.rollback()

    def test_insert_record(self):
        u = Article(title='title')
        key = database.insert_record(u)
        self.assertTrue(key)

    def test_update_record(self):
        u = Article(title='title')
        u.save()

        u.title = "something"

        key = database.update_record(u)

        u2 = Article.get(u.key)

        self.assertTrue(u.title == u2.title)
        self.assertTrue(u2.title != 'title')

    def test_delete_record(self):
        a = Article(title='sometitle')
        key = a.save()

        database.delete_record(a)

        a2 = Article.get(key)

        self.assertTrue(a2 is None)
        self.assertTrue(a.key is None)

