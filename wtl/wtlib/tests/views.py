from __future__ import unicode_literals

from django.test import TestCase

from wtl.wtlib.forms import AnalyzeForm
from wtl.wtlib.tests.factories import LibraryFactory, ProjectFactory


class HomeTestCase(TestCase):
    def test_template(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'wtlib/home.html')
        self.assertTemplateUsed(response, 'wtlib/_repo_form.html')

    def test_form_passed_on_get(self):
        response = self.client.get('/')
        self.assertEqual(response.context['analyze_form'].__class__,
                         AnalyzeForm)

    def test_repo_id_required(self):
        response = self.client.post('/', {'git_url': ''})
        self.assertFormError(response, 'analyze_form', 'git_url',
                             'This field is required.')

    def test_repo_not_exists(self):
        response = self.client.post('/', {'git_url': 'foo'})
        self.assertFormError(response, 'analyze_form', 'git_url',
                             'Repository not found.')


class LibrariesListTestCase(TestCase):
    def test_template(self):
        response = self.client.get('/libraries/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'wtlib/libraries_list.html')


class LibraryTestCase(TestCase):
    def test_template(self):
        lib = LibraryFactory()
        url = '/libraries/{0}/{1}'.format(lib.language.slug, lib.slug)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'wtlib/library.html')


class ProjectsListTestCase(TestCase):
    def test_template(self):
        response = self.client.get('/projects/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'wtlib/projects_list.html')


class ProjectTestCase(TestCase):
    def test_template(self):
        project = ProjectFactory()
        response = self.client.get('/projects/{0}'.format(project.slug))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'wtlib/project.html')
