from __future__ import unicode_literals
import os
import re
import sys
if sys.version_info >= (3,):
    import urllib.request as urllib2
else:
    import urllib2

from django.test import TestCase
from exam.asserts import AssertsMixin
import mock

from wtl.wtlib.tests.factories import LanguageFactory, LibraryFactory
from wtl.wtlib.models import Library
from wtl.wtparser.parsers import RequirementsParser


REQUIREMENTS = """
# Example requirements.txt
Django==1.5.4
south>=0.8.2
gondor
gunicorn>=18.0,<19
-e git+git://github.com/user/package#egg=package
"""

class BaseTestCase(TestCase):
    def setUp(self):
        super(BaseTestCase, self).setUp()
        self.parser = RequirementsParser()
        LanguageFactory(name=self.parser.language)


class RequirementsGuessTestCase(BaseTestCase):
    def test_requirements(self):
        self.assertTrue(self.parser.detect(REQUIREMENTS))

    def test_unknown(self):
        content = "#include <iostream>"
        self.assertFalse(self.parser.detect(content))


class RequirementsParseTestCase(BaseTestCase):
    maxDiff = None
    def setUp(self):
        super(RequirementsParseTestCase, self).setUp()
        self.parser._get_package_info = lambda x: ''

    def test_requirements(self):
        expect = {
            'filename': self.parser.filename,
            'language': self.parser.language,
            'platform': None,
            'version':  None,
            'packages': [
                {'name': 'Django',
                 'version': '1.5.4',
                 'version_special': ''},
                {'name': 'south',
                 'version': '0.8.2',
                 'version_special': '>='},
                {'name': 'gondor',
                 'version': None,
                 'version_special': 'stable'},
                {'name': 'gunicorn',
                 'version': '18.0',
                 'version_special': '>='},
                {'name': 'package',
                 'version': None,
                 'version_special': 'latest'},
            ],
        }
        self.assertEqual(self.parser.parse(REQUIREMENTS), expect)


class GetPackageInfoTestCase(BaseTestCase, AssertsMixin):
    def setUp(self):
        super(GetPackageInfoTestCase, self).setUp()

        def urlopenMock(request, timeout):
            filename = re.sub('\/json$', '.json', request.selector).lstrip('/')
            path = os.path.join(os.path.dirname(__file__), 'test_responses', filename)
            if not os.path.exists(path):
                raise urllib2.HTTPError(request.full_url, 404, 'not found', {}, None)
            return open(path, 'rb')
        if sys.version_info >= (3,):
            self.urllibPatch = mock.patch('urllib.request.urlopen', urlopenMock)
        else:
            self.urllibPatch = mock.patch('urllib2.urlopen', urlopenMock)
        self.urllibPatch.start()

    def tearDown(self):
        super(GetPackageInfoTestCase, self).tearDown()
        self.urllibPatch.stop()

    def test_creates_library(self):
        with self.assertChanges(Library.objects.count, before=0, after=1):
            self.parser._get_package_info('django')
        library = Library.objects.get(name='django')
        self.assertEqual('http://www.djangoproject.com/', library.url_home)
        self.assertEqual('', library.url_docs)
        self.assertEqual('A high-level Python Web framework that encourages rapid development and clean, pragmatic design.', library.short_description)
        self.assertEqual('BSD', library.license)

    def test_does_nothing_if_library_exist(self):
        LibraryFactory(language=self.parser.language_instance, name='django')
        with self.assertDoesNotChange(Library.objects.count):
            self.parser._get_package_info('django')

    def test_returns_none_on_http_error(self):
        with self.assertDoesNotChange(Library.objects.count):
            res = self.parser._get_package_info('no_such_packages')
        self.assertIsNone(res)
