from __future__ import unicode_literals
import logging
import sys
if sys.version_info >= (3,):
    import urllib.request as urllib2
else:
    import urllib2

from django.template.defaultfilters import slugify
from django.utils.functional import cached_property
from wtl.wtlib.models import Language, Library

from pkgtools.pypi import PyPIJson
import requirements

from wtl.wtparser.parsers.base import BaseParser


logger = logging.getLogger(__name__)


class RequirementsParser(BaseParser):
    language = 'Python'
    filename = 'requirements.txt'

    @cached_property
    def language_instance(self):
        return Language.objects.get(name=self.language)

    def detect(self, content):
        res = [
            r'''^--index-url ''',
            r'''^-i ''',
            r'''^--no-index''',
            r'''^--extra-index-url ''',
            r'''^--find-links ''',
            r'''^-f ''',
            r'''^-r ''',
            r'''^-e ''',
            r'''^\w.*[=<>]+''',
        ]
        return self._detect_by_regex(content, res)

    def get_packages(self, lines):
        reqs = requirements.parse('\n'.join(lines))
        return [self._get_req(r) for r in reqs if not r.local_file and r.name]

    def _get_package_info(self, package_name):
        library_name = package_name.lower()
        try:
            #TODO: update library info
            return Library.objects.get(language=self.language_instance, name=library_name)
        except Library.DoesNotExist:
            pass

        logger.debug('Retrieving packge info from pypi: %s', package_name)
        def _request(url, timeout=None):
            r = urllib2.Request(url)
            return urllib2.urlopen(r, timeout=timeout).read().decode('utf-8')
        try:
            # TODO: get rid of fast=true (need to normalize package name)
            json = PyPIJson(package_name, fast=True).retrieve(_request)
            logger.debug('Retrieved data from pypi, saving to database...')
        except urllib2.HTTPError:
            return None
        library = Library.objects.create(language=self.language_instance,
                                         name=library_name,
                                         slug=slugify(json['info']['name']),
                                         short_description=json['info']['summary'],
                                         license=json['info']['license'],
                                         url_home=json['info']['home_page'],
                                         url_docs=json['info']['docs_url'],
                                         url_repo='')
        return library

    def _get_req(self, req):
        if len(req.specs) > 0 and not req.vcs:
            version = req.specs[0][1]
            special = req.specs[0][0] if req.specs[0][0] != '==' else ''
        elif len(req.specs) == 0 and not req.vcs:
            version = None
            special = 'stable'
        elif req.vcs:
            version = None
            special = 'latest'
        self._get_package_info(req.name)
        return {'name': req.name,
                'version': version,
                'version_special': special}
