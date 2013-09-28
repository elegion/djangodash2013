from __future__ import unicode_literals

from django.test import TestCase

from .factories import LibraryFactory, LibraryVersionFactory


class LibraryTestCase(TestCase):
    def test_str(self):
        x = LibraryFactory()
        self.assertEqual(str(x), x.name)
