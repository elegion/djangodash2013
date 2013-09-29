from __future__ import unicode_literals

from django.test import TestCase

from wtl.wtlib.models import Library, LibraryVersion
from wtl.wtlib.tests.factories import (LibraryFactory, LibraryVersionFactory,
                                       ProjectFactory)


class LibraryTestCase(TestCase):
    def test_str(self):
        x = LibraryFactory()
        self.assertEqual(str(x), x.name)


class LibraryVersionTestCase(TestCase):
    def test_str(self):
        x = LibraryVersionFactory()
        self.assertEqual(str(x), x.library.name + ' ' + x.version)

    def test_update_totals(self):
        l1 = LibraryFactory(name='l1')
        l1v1 = LibraryVersionFactory(library=l1, version="1")
        l1v2 = LibraryVersionFactory(library=l1, version="2")
        l2 = LibraryFactory(name='l2')
        l2v1 = LibraryVersionFactory(library=l2, version="1")
        l2v2 = LibraryVersionFactory(library=l2, version="2")
        p = ProjectFactory()
        p.libraries.add(l1v1)
        p.libraries.add(l1v2)
        p.libraries.add(l2v1)
        LibraryVersion.update_totals_by_project(p)

        self.assertEqual(Library.objects.get(id=l1.id).total_users, 2)
        self.assertEqual(Library.objects.get(id=l2.id).total_users, 1)
        self.assertEqual(LibraryVersion.objects.get(id=l1v1.id).total_users, 1)
        self.assertEqual(LibraryVersion.objects.get(id=l1v2.id).total_users, 1)
        self.assertEqual(LibraryVersion.objects.get(id=l2v1.id).total_users, 1)
        self.assertEqual(LibraryVersion.objects.get(id=l2v2.id).total_users, 0)


class ProjectTestCase(TestCase):
    def test_str(self):
        x = ProjectFactory()
        self.assertEqual(str(x), x.name)
