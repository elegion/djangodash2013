from __future__ import unicode_literals

from django.test import TestCase

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


class RequirementsGuessTestCase(BaseTestCase):
    def test_requirements(self):
        self.assertTrue(self.parser.detect(REQUIREMENTS))

    def test_unknown(self):
        content = "#include <iostream>"
        self.assertFalse(self.parser.detect(content))


class RequirementsParseTestCase(BaseTestCase):
    maxDiff = None

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
