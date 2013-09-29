from __future__ import unicode_literals

from django.test import TestCase

from wtl.wtlib.tests.factories import LibraryFactory, LibraryVersionFactory


class LibraryTestCase(TestCase):
    def test_str(self):
        x = LibraryFactory()
        self.assertEqual(str(x), x.name)


class LibraryVersionTestCase(TestCase):
    def test_str(self):
        x = LibraryVersionFactory()
        self.assertEqual(str(x), x.library.name + ' ' + x.version)
