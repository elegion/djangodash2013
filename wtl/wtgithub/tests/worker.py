from __future__ import unicode_literals
import os

from django.test import TestCase
from exam.asserts import AssertsMixin
from github import UnknownObjectException
from github.Requester import Requester
import mock

from wtl.wtgithub.models import Repository
from wtl.wtgithub.tests.factories import RepositoryFactory
from wtl.wtgithub.worker import GithubWorker, CantFindParserError, ParseError
from wtl.wtlib.factories import ProjectFactory, LibraryFactory, LibraryVersionFactory, LanguageFactory
from wtl.wtlib.models import Project, Library, LibraryVersion
from wtl.wtparser.parsers import RequirementsParser


class BaseTestCase(TestCase):
    def setUp(self):
        super(BaseTestCase, self).setUp()
        self.language = LanguageFactory(name='Python')
        # Mock github requests
        self.connectionMock = mock.Mock()
        connectionClass = mock.Mock()
        connectionClass.return_value = self.connectionMock
        Requester.injectConnectionClasses(connectionClass, connectionClass)

        self.worker = GithubWorker()
        # preload gh_rep used by most tests
        self.githubWillRespondWith('get_repo/elegion__djangodash2013.json')
        self.gh_rep = self.worker.github.get_repo('elegion/djangodash2013')

    def tearDown(self):
        super(BaseTestCase, self).tearDown()
        Requester.resetConnectionClasses()

    def githubWillRespondWith(self, filename, response_code=200):
        """
        Instead of requesting to github, respond with contents of test_responses/$filename file
        """
        content = open(os.path.join(os.path.dirname(__file__), 'test_responses', filename)).read()
        response = mock.Mock()
        type(response).status = mock.PropertyMock(return_value=response_code)
        response.getheaders.return_value = {}
        response.read.return_value = content
        self.connectionMock.getresponse.return_value = response


class GetParserForRepositoryTestCase(BaseTestCase):
    def test_returns_parser(self):
        self.githubWillRespondWith('get_git_tree/elegion__djangodash2013.json')
        sha, parser = self.worker._get_parser_for_repository(self.gh_rep)
        self.assertIsInstance(parser, RequirementsParser)
        self.assertEqual(40, len(sha))

    def test_returns_none(self):
        self.githubWillRespondWith('get_git_tree/github__objective-c-conventions.json')
        with self.assertRaises(CantFindParserError):
            self.worker._get_parser_for_repository(self.gh_rep)


class GetOrCreateRepositoryTestCase(BaseTestCase, AssertsMixin):
    def test_creates_repository(self):
        with self.assertChanges(Repository.objects.count, before=0, after=1):
            self.worker._get_or_create_repository(self.gh_rep)

        repository = Repository.objects.all()[0]

        self.assertEqual('elegion', repository.owner)
        self.assertEqual('djangodash2013', repository.name)

    def test_updates_existing_repository(self):
        RepositoryFactory(name='djangodash2013',
                          owner='elegion',
                          starsCount=100)

        with self.assertDoesNotChange(Repository.objects.count):
            self.worker._get_or_create_repository(self.gh_rep)

        repository = Repository.objects.all()[0]

        self.assertEqual('elegion', repository.owner)
        self.assertEqual('djangodash2013', repository.name)
        self.assertEqual(0, repository.starsCount)

    def test_creates_project_if_not_exist(self):
        with self.assertChanges(Project.objects.count, before=0, after=1):
            self.worker._get_or_create_repository(self.gh_rep)

        project = Project.objects.all()[0]

        self.assertEqual('djangodash2013', project.name)
        self.assertEqual('djangodash2013', project.github.name)
        self.assertEqual('elegion', project.github.owner)

    def test_creates_project_even_if_repository_exists(self):
        RepositoryFactory(name='djangodash2013',
                          owner='elegion',
                          starsCount=100)

        with self.assertChanges(Project.objects.count, before=0, after=1):
            self.worker._get_or_create_repository(self.gh_rep)

        project = Project.objects.all()[0]

        self.assertEqual('djangodash2013', project.name)
        self.assertEqual('djangodash2013', project.github.name)
        self.assertEqual('elegion', project.github.owner)


class ParseRequirementsTestCase(BaseTestCase):
    def test_returns_parsed_requirements(self):
        parser = mock.Mock()
        parser.parse.return_value = {'language': self.language}
        self.githubWillRespondWith('get_git_blog/requrements.txt.json')
        res = self.worker._parse_requirements(self.gh_rep, 'bbdce0004a897ba617f1001591c7dea665485425', parser)
        self.assertIsInstance(res, dict)
        self.assertDictEqual(parser.parse.return_value, res)

    def test_raises_parse_error(self):
        parser = mock.Mock()
        parser.parse.side_effect = ValueError('some parse error')
        self.githubWillRespondWith('get_git_blog/invalid-requirements.txt.json')
        with self.assertRaises(ParseError):
            self.worker._parse_requirements(self.gh_rep, 'dd3705261c05bd3d3609de15bff66b6b4a5dd0ad', parser)


class SaveParsedRequirementsTestCase(BaseTestCase, AssertsMixin):
    def sampleDict(self):
        return {
            'platform': None,
            'language': self.language.name,
            'packages': [
                {'name': 'django', 'version': '1.5.4', 'version_special': ''},
                {'name': 'south', 'version': '0.8.2', 'version_special': ''},
            ],
            'version': None,
            'filename': 'requirements.txt'
        }

    def test_saves_packages_and_versions(self):
        project = ProjectFactory()
        with self.assertChanges(Library.objects.count, before=0, after=2):
            with self.assertChanges(LibraryVersion.objects.count, before=0, after=2):
                self.worker._save_parsed_requirements(project, self.sampleDict())
        self.assertEqual(2, project.libraries.count())
        lib1 = project.libraries.order_by('library__name')[0]
        lib2 = project.libraries.order_by('library__name')[1]
        self.assertEqual('django', lib1.library.name)
        self.assertEqual('1.5.4', lib1.version)
        self.assertEqual(1, lib1.total_users)
        self.assertEqual('south', lib2.library.name)
        self.assertEqual('0.8.2', lib2.version)
        self.assertEqual(1, lib2.total_users)

    def test_updates_total_users_count(self):
        l1 = LibraryFactory(name='django', language=self.language)
        l2 = LibraryFactory(name='south', language=self.language)
        self.worker._save_parsed_requirements(ProjectFactory(),
                                              self.sampleDict())

        self.assertEqual(Library.objects.get(id=l1.id).total_users, 1)
        self.assertEqual(LibraryVersion.objects.get(library=l1).total_users, 1)
        self.assertEqual(Library.objects.get(id=l2.id).total_users, 1)
        self.assertEqual(LibraryVersion.objects.get(library=l2).total_users, 1)

    def test_doesnt_duplicate_libraries_and_versions(self):
        project = ProjectFactory()
        lib1 = LibraryFactory(name='django', language=self.language)
        lib2 = LibraryFactory(name='south', language=self.language)
        LibraryVersionFactory(library=lib1, version='1.5.4')
        LibraryVersionFactory(library=lib2, version='0.8.2')
        with self.assertDoesNotChange(Library.objects.count,):
            with self.assertDoesNotChange(LibraryVersion.objects.count):
                self.worker._save_parsed_requirements(project, self.sampleDict())
        self.assertEqual(2, project.libraries.count())


class AnalyzeRepoTestCase(BaseTestCase):
    def test_called_with_invalid_url(self):
        self.githubWillRespondWith('404.json', response_code=404)
        with self.assertRaises(UnknownObjectException):
            self.worker.analyze_repo('invalid/url')
