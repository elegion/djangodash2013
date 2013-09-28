from django.conf import settings
from github import Github

from wtl.wtgithub.models import Repository
from wtl.wtlib.models import Project


class GithubWorker(object):
    github = None

    def __init__(self, github=None):
        super().__init__()
        if github is None:
            self.github = Github(getattr(settings, 'WTGITHUB_USERNAME', None),
                                 getattr(settings, 'WTGITHUB_PASSWORD', None))
        if github is not None:
            self.github = github

    def analyze_repo(self, full_name):
        rep = self.github.get_repo(full_name)

        try:
            repository = Repository.objects.get(name=rep.name,
                                                owner=rep.owner._identity)
        except Repository.DoesNotExist:
            repository = Repository(name=rep.name, owner=rep.owner._identity)
        repository.starsCount = rep.watchers
        repository.description = rep.description
        repository.save()
        try:
            repository.project
        except Project.DoesNotExist:
            Project.objects.create(github=repository, name=rep.name)
        return repository
