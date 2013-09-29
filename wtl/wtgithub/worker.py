import base64
import logging

from django.conf import settings

from wtl.wtgithub.github import WtGithub
from wtl.wtgithub.models import Repository
from wtl.wtlib.models import Project, Library, LibraryVersion, Language
from wtl.wtparser.parser import get_parser_for_filename


logger = logging.getLogger(__name__)


class WorkerError(Exception):
    """
    Base class for all worker exceptions.
    """


class CantFindParserError(WorkerError):
    """
    Raised when can't find requirements file in given repository.
    """


class ParseError(WorkerError):
    """
    Raised when parser can't parse requirements file.
    """
    def __init__(self, error=None, *args, **kwargs):
        super(ParseError, self).__init__(*args, **kwargs)
        self.error = error


class BaseGithubWorker(object):
    github = None

    def __init__(self, github=None, per_page=None):
        super(BaseGithubWorker, self).__init__()
        if github is None:
            if per_page is None:
                per_page = getattr(settings, 'WTGITHUB_PER_PAGE', 30)
            github = WtGithub(getattr(settings, 'WTGITHUB_USERNAME', None),
                              getattr(settings, 'WTGITHUB_PASSWORD', None),
                              per_page=per_page)
        self.github = github


class GithubWorker(BaseGithubWorker):
    def _get_repo(self, full_name):
        """
        Fetches GitHub repository information.
        """
        return self.github.get_repo(full_name)

    def _get_or_create_repository(self, rep):
        """
        Creates (if does not exist) and returns:
        `wtgithub.models.Repository` and `wtlib.models.Project`.
        """
        try:
            repository = Repository.objects.get(name=rep.name,
                                                owner=rep.owner._identity)
            logger.info('Repository already exists in database, updating...')
        except Repository.DoesNotExist:
            logger.info('No repository in database, creating...')
            repository = Repository(name=rep.name, owner=rep.owner._identity)
        repository.starsCount = rep.watchers
        repository.description = rep.description
        repository.save()
        logger.info('Repository info saved(updated)')
        try:
            project = repository.project
            logger.info('Project already exists in database')
        except Project.DoesNotExist:
            logger.info('No project in database, creating...')
            project = Project.objects.create(github=repository, name=rep.name)
        return repository, project

    def _get_parser_for_repository(self, rep):
        """
        Analyzes repository tree to find corresponding requirements parser.
        Currently analyzes only repository root and returns first matching
        parser. Raises `CantFindParserError` if can't determine parser for
        given repository.
        """
        logger.info('Trying to get parser for repository')
        logger.info('Receiving repository tree...')
        tree = rep.get_git_tree('master')
        logger.info('Received repository tree from github (%i items)', len(tree.tree))
        for node in tree.tree:
            if node.type != 'blob':
                continue
            parser = get_parser_for_filename(node.path)
            if parser is not None:
                logger.info('Determined parser for file %s: %s', node.path, node)
                return node.sha, parser
        logger.warning('Failed to determine parser for repository. Stopping analysis.')
        raise CantFindParserError()

    def _parse_requirements(self, rep, blob_sha, parser):
        """
        Parses requirements file in given repository with given parser
        Raises `ParseError` if parse fails.
        """
        logger.info('Retrieving requirements file from repository...')
        blob = rep.get_git_blob(blob_sha)
        logger.info('Received file, decoding...')
        if blob.encoding == 'utf-8':
            content = blob.content
        elif blob.encoding == 'base64':
            try:
                content = base64.b64decode(blob.content).decode('utf-8')
            except BaseException as e:
                logger.error('Error decoding file: %s', e.__repr__())
                raise ParseError('Error decoding blob')
        else:
            logger.error('Error decoding file. Unknown encoding: %s', blob.encoding)
            raise ParseError('Unknown blob encoding')
        try:
            logger.info('Decoded file, length: %s bytes', len(content))
            logger.info('Starting file parsing...')
            res = parser.parse(content)
            logger.info('Finished parsing requirements! %i dependencies found.', len(res['packages']))
            return res
        except Exception as e:
            logger.error('Error parsing file: %s', e.__repr__())
            raise ParseError(error=e)

    def _save_parsed_requirements(self, project, parsed):
        """
        Saves parsed requirements to database.
        """
        logger.info('Start saving parsed requirements')
        language = Language.objects.get(name=parsed['language'])
        for package_dict in parsed['packages']:
            library, _ = Library.objects.get_or_create(
                language=language, name=package_dict['name'])
            version, _ = LibraryVersion.objects.get_or_create(
                library=library, version=package_dict['version'],
                version_special=package_dict['version_special'])
            version.save()
            project.libraries.add(version)
        logger.info('Saved parsed requirements')
        self._update_user_counts(project)

    def _update_user_counts(self, project):
        LibraryVersion.update_totals(project=project)

    def analyze_repo(self, full_name=None, rep=None):
        if rep is None:
            logger.info('Start analyzing repo %s', full_name)
            rep = self._get_repo(full_name)
        else:
            logger.info('Start analyzing repo %s', rep.full_name)
        repository, project = self._get_or_create_repository(rep)
        requirements_blob_sha, parser = self._get_parser_for_repository(rep)
        parsed = self._parse_requirements(rep, requirements_blob_sha, parser)
        self._save_parsed_requirements(project, parsed)
        logger.info('Finished analyzing repo!')
        return repository, project


class GithubBulkWorker(BaseGithubWorker):
    def __init__(self, github=None, per_page=None):
        if per_page is None:
            per_page = getattr(settings, 'WTGITHUB_SEARCH_PER_PAGE', 100)
        super(GithubBulkWorker, self).__init__(github, per_page)
        self.github_worker = GithubWorker(github)

    def _get_repositories(self, language):
        logger.info('Preparing request for api.github.com/search/repositories')
        return self.github.search_repos('language:%s' % language)

    def _check_repository_analyzed(self, rep):
        return Project.objects.filter(github__name=rep.name,
                                      github__owner=rep.owner._identity).count() != 0

    def analyze_repos(self, language, count=100):
        logger.info('Start analyzing repositories for language: %s', language)
        repositories = self._get_repositories(language)
        analyzed_repos = 0
        for rep in repositories:
            logger.debug('Will analyze repository: %s', rep.full_name)
            if self._check_repository_analyzed(rep):
                logger.debug('Already analysed, skipping...')
                continue
            analyzed_repos += 1
            try:
                self.github_worker.analyze_repo(rep=rep)
            except BaseException as e:
                logger.error('Error analysing repository: %s', e.__repr__())
            else:
                logger.debug('Analysed repository successfully. %i to go...', count-analyzed_repos)
