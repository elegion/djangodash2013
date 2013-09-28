from django.conf import settings
from github import Github

from wtl.wtgithub.models import Repository
from wtl.wtlib.models import Project
from wtl.wtparser.parser import get_parser_for_filename


class WorkerError(BaseException):
    """
    Base class for all worker exceptions
    """
    pass


class CantFindParserError(WorkerError):
    """
    Raised when can't find requirements file in given repository
    """
    pass


class GithubWorker(object):
    github = None

    def __init__(self, github=None):
        super().__init__()
        if github is None:
            self.github = Github(getattr(settings, 'WTGITHUB_USERNAME', None),
                                 getattr(settings, 'WTGITHUB_PASSWORD', None))
        if github is not None:
            self.github = github

    def _get_or_create_repository(self, rep):
        """
        Fetches github repository information, creates `wtgithub.models.Repository`
        and `wtlib.models.Project` if does not exist.
        Returns github repository information and `wtgithub.models.Repository`
        """
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
        return rep, repository

    def _get_parser_for_repository(self, rep):
        """
        Analyzes repository tree to find corresponding requirements parser.
        Currently analyzes only repository root and returns first matching parser.
        Raises CantFindParserError if can't determine parser for given repository.
        """
        tree = rep.get_git_tree('master')
        for node in tree.tree:
            if node.type != 'blob':
                continue
            parser = get_parser_for_filename(node.path)
            if parser is not None:
                return parser
        raise CantFindParserError()

    def analyze_repo(self, full_name):
        rep = self.github.get_repo(full_name)
        repository = self._get_or_create_repository(rep)
        parser = self._get_parser_for_repository(rep)
