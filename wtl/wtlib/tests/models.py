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
        LibraryVersion.update_totals(project=p)

        self.assertEqual(Library.objects.get(id=l1.id).total_users, 2)
        self.assertEqual(Library.objects.get(id=l2.id).total_users, 1)
        self.assertEqual(LibraryVersion.objects.get(id=l1v1.id).total_users, 1)
        self.assertEqual(LibraryVersion.objects.get(id=l1v2.id).total_users, 1)
        self.assertEqual(LibraryVersion.objects.get(id=l2v1.id).total_users, 1)
        self.assertEqual(LibraryVersion.objects.get(id=l2v2.id).total_users, 0)

    def test_often_used_with(self):
        lib1 = LibraryFactory()
        lib2 = LibraryFactory()
        lib3 = LibraryFactory()
        lib4 = LibraryFactory()
        ver1 = LibraryVersionFactory(library=lib1)

        project_1_2 = ProjectFactory()
        project_1_2.libraries.add(ver1)
        project_1_2.libraries.add(LibraryVersionFactory(library=lib2))

        project_1_2__2 = ProjectFactory()
        project_1_2__2.libraries.add(ver1)
        project_1_2__2.libraries.add(LibraryVersionFactory(library=lib2))

        project_1_3 = ProjectFactory()
        project_1_3.libraries.add(LibraryVersionFactory(library=lib1))
        project_1_3.libraries.add(LibraryVersionFactory(library=lib3))

        project_2_3_4 = ProjectFactory()
        project_2_3_4.libraries.add(LibraryVersionFactory(library=lib2))
        project_2_3_4.libraries.add(LibraryVersionFactory(library=lib3))
        project_2_3_4.libraries.add(LibraryVersionFactory(library=lib4))

        lib1_result = lib1.often_used_with()
        self.assertEqual(lib2.name, lib1_result[0].name)
        self.assertEqual(2, lib1_result[0].usage_count)
        self.assertEqual(lib3.name, lib1_result[1].name)
        self.assertEqual(1, lib1_result[1].usage_count)


class ProjectTestCase(TestCase):
    def test_str(self):
        x = ProjectFactory()
        self.assertEqual(str(x), x.name)
