from __future__ import unicode_literals

from django.test import TestCase
from exam.asserts import AssertsMixin
from github import UnknownObjectException

from wtl.wtgithub.models import Repository
from wtl.wtgithub.tests.factories import RepositoryFactory
from wtl.wtgithub.worker import GithubWorker
from wtl.wtlib.models import Project


class AnalyzeRepoTestCase(TestCase, AssertsMixin):
    def setUp(self):
        self.worker = GithubWorker()

    def test_called_with_invalid_url(self):
        with self.assertRaises(UnknownObjectException):
            self.worker.analyze_repo('invalid/url')

    def test_creates_repository(self):
        with self.assertChanges(Repository.objects.count, before=0, after=1):
            self.worker.analyze_repo('elegion/djangodash2013')

        repository = Repository.objects.all()[0]

        self.assertEqual('elegion', repository.owner)
        self.assertEqual('djangodash2013', repository.name)

    def test_updates_existing_repository(self):
        RepositoryFactory(name='djangodash2013',
                          owner='elegion',
                          starsCount=100)

        with self.assertDoesNotChange(Repository.objects.count):
            self.worker.analyze_repo('elegion/djangodash2013')

        repository = Repository.objects.all()[0]

        self.assertEqual('elegion', repository.owner)
        self.assertEqual('djangodash2013', repository.name)
        self.assertEqual(0, repository.starsCount)

    def test_creates_project_if_not_exist(self):
        with self.assertChanges(Project.objects.count, before=0, after=1):
            self.worker.analyze_repo('elegion/djangodash2013')

        project = Project.objects.all()[0]

        self.assertEqual('djangodash2013', project.name)
        self.assertEqual('djangodash2013', project.github.name)
        self.assertEqual('elegion', project.github.owner)

    def test_creates_project_even_if_repository_exists(self):
        RepositoryFactory(name='djangodash2013',
                          owner='elegion',
                          starsCount=100)

        with self.assertChanges(Project.objects.count, before=0, after=1):
            self.worker.analyze_repo('elegion/djangodash2013')

        project = Project.objects.all()[0]

        self.assertEqual('djangodash2013', project.name)
        self.assertEqual('djangodash2013', project.github.name)
        self.assertEqual('elegion', project.github.owner)
