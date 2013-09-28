from __future__ import unicode_literals

from django.test import TestCase
from github import Github

from .factories import LibraryFactory, LibraryVersionFactory


class LibraryTestCase(TestCase):
    def test_str(self):

        x = LibraryFactory()
        self.assertEqual(str(x), x.name)


class LibraryVersionTestCase(TestCase):
    def test_str(self):
        x = LibraryVersionFactory()
        self.assertEqual(str(x), x.library.name + ' ' + x.version)


class HomeTestCase(TestCase):
    def test_template(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed('wtlib/home.html')
        self.assertTemplateUsed('wtlib/_repo_form.html')
