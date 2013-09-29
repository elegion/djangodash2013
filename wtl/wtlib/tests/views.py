from __future__ import unicode_literals

from django.test import TestCase

from wtl.wtlib.forms import AnalyzeForm
from wtl.wtlib.tests.factories import (LanguageFactory, LibraryFactory,
                                       LibraryVersionFactory, ProjectFactory)


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

    def test_active_menu(self):
        response = self.client.get('/')
        self.assertNotIn('active_menu', response.context)
        self.assertNotIn('active_language', response.context)


class LibrariesListTestCase(TestCase):
    def test_template(self):
        response = self.client.get('/libraries/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'wtlib/libraries_list.html')

    def test_mixed_output_var(self):
        lang1 = LanguageFactory()
        response = self.client.get('/libraries/')
        self.assertTrue(response.context['mixed_languages'])
        response = self.client.get('/libraries/{0}/'.format(lang1.slug))
        self.assertFalse(response.context['mixed_languages'])

    def test_language_filter(self):
        lang1 = LanguageFactory()
        lang2 = LanguageFactory()
        lib1 = LibraryFactory(language=lang1)
        lib2 = LibraryFactory(language=lang2)

        response = self.client.get('/libraries/')
        self.assertItemsEqual(response.context['libraries'], [lib1, lib2])
        response = self.client.get('/libraries/{0}/'.format(lang1.slug))
        self.assertItemsEqual(response.context['libraries'], [lib1])
        response = self.client.get('/libraries/{0}/'.format(lang2.slug))
        self.assertItemsEqual(response.context['libraries'], [lib2])

    def test_active_menu(self):
        lang = LanguageFactory()
        response = self.client.get('/libraries/')
        self.assertEqual(response.context['active_menu'], 'libraries')
        self.assertEqual(response.context['active_language'], None)
        response = self.client.get('/libraries/{0}/'.format(lang.slug))
        self.assertEqual(response.context['active_menu'], 'libraries')
        self.assertEqual(response.context['active_language'], lang.slug)


class LibraryTestCase(TestCase):
    def test_template(self):
        lib = LibraryFactory()
        url = '/libraries/{0}/{1}'.format(lib.language.slug, lib.slug)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'wtlib/library.html')

    def test_active_menu(self):
        lib = LibraryFactory()
        url = '/libraries/{0}/{1}'.format(lib.language.slug, lib.slug)
        response = self.client.get(url)
        self.assertEqual(response.context['active_menu'], 'libraries')
        self.assertEqual(response.context['active_language'],
                         lib.language.slug)


class ProjectsListTestCase(TestCase):
    def test_template(self):
        response = self.client.get('/projects/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'wtlib/projects_list.html')

    def test_language_filter(self):
        lang1 = LanguageFactory()
        lang2 = LanguageFactory()
        v1 = LibraryVersionFactory(library=LibraryFactory(language=lang1))
        v2 = LibraryVersionFactory(library=LibraryFactory(language=lang2))
        proj1 = ProjectFactory()
        proj1.libraries.add(v1)
        proj2 = ProjectFactory()
        proj2.libraries.add(v2)

        response = self.client.get('/projects/')
        self.assertItemsEqual(response.context['projects'], [proj1, proj2])
        response = self.client.get('/projects/{0}/'.format(lang1.slug))
        self.assertItemsEqual(response.context['projects'], [proj1])
        response = self.client.get('/projects/{0}/'.format(lang2.slug))
        self.assertItemsEqual(response.context['projects'], [proj2])

    def test_active_menu(self):
        lang = LanguageFactory()
        response = self.client.get('/projects/')
        self.assertEqual(response.context['active_menu'], 'projects')
        self.assertEqual(response.context['active_language'], None)
        response = self.client.get('/projects/{0}/'.format(lang.slug))
        self.assertEqual(response.context['active_menu'], 'projects')
        self.assertEqual(response.context['active_language'], lang.slug)


class ProjectTestCase(TestCase):
    def test_template(self):
        project = ProjectFactory()
        project.libraries.add(LibraryVersionFactory())
        url = '/projects/{0}/{1}'.format(project.language_slug, project.slug)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'wtlib/project.html')

    def test_active_menu(self):
        project = ProjectFactory()
        project.libraries.add(LibraryVersionFactory())
        url = '/projects/{0}/{1}'.format(project.language_slug, project.slug)
        response = self.client.get(url)
        self.assertEqual(response.context['active_menu'], 'projects')
        self.assertEqual(response.context['active_language'],
                         project.language_slug)
