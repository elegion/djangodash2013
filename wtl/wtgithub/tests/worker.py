from __future__ import unicode_literals

from django.test import TestCase
from exam.asserts import AssertsMixin
from github import Github, UnknownObjectException

from wtl.wtgithub.models import Repository
from wtl.wtgithub.tests.factories import RepositoryFactory
from wtl.wtgithub.worker import GithubWorker, CantFindParserError
from wtl.wtlib.models import Project
from wtl.wtparser.parsers import RequirementsParser


gh_rep = None
def setUpModule():
    global gh_rep
    github = Github()
    gh_rep = github.get_repo('elegion/djangodash2013')


class BaseTestCase(TestCase):
    def setUp(self):
        self.worker = GithubWorker()
        super(BaseTestCase, self).setUp()


class GetParserForRepositoryTestCase(BaseTestCase):
    def test_returns_parser(self):
        parser = self.worker._get_parser_for_repository(gh_rep)
        self.assertIsInstance(parser, RequirementsParser)

    def test_returns_none(self):
        github = Github()
        repo = github.get_repo('github/objective-c-conventions')
        with self.assertRaises(CantFindParserError):
            self.worker._get_parser_for_repository(repo)


class GetOrCreateRepositoryTestCase(BaseTestCase, AssertsMixin):
    def test_creates_repository(self):
        with self.assertChanges(Repository.objects.count, before=0, after=1):
            self.worker._get_or_create_repository(gh_rep)

        repository = Repository.objects.all()[0]

        self.assertEqual('elegion', repository.owner)
        self.assertEqual('djangodash2013', repository.name)

    def test_updates_existing_repository(self):
        RepositoryFactory(name='djangodash2013',
                          owner='elegion',
                          starsCount=100)

        with self.assertDoesNotChange(Repository.objects.count):
            self.worker._get_or_create_repository(gh_rep)

        repository = Repository.objects.all()[0]

        self.assertEqual('elegion', repository.owner)
        self.assertEqual('djangodash2013', repository.name)
        self.assertEqual(0, repository.starsCount)

    def test_creates_project_if_not_exist(self):
        with self.assertChanges(Project.objects.count, before=0, after=1):
            self.worker._get_or_create_repository(gh_rep)

        project = Project.objects.all()[0]

        self.assertEqual('djangodash2013', project.name)
        self.assertEqual('djangodash2013', project.github.name)
        self.assertEqual('elegion', project.github.owner)

    def test_creates_project_even_if_repository_exists(self):
        RepositoryFactory(name='djangodash2013',
                          owner='elegion',
                          starsCount=100)

        with self.assertChanges(Project.objects.count, before=0, after=1):
            self.worker._get_or_create_repository(gh_rep)

        project = Project.objects.all()[0]

        self.assertEqual('djangodash2013', project.name)
        self.assertEqual('djangodash2013', project.github.name)
        self.assertEqual('elegion', project.github.owner)


class AnalyzeRepoTestCase(BaseTestCase):
    def test_called_with_invalid_url(self):
        with self.assertRaises(UnknownObjectException):
            self.worker.analyze_repo('invalid/url')
