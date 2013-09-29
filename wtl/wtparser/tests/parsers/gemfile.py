from __future__ import unicode_literals

from django.test import TestCase

from wtl.wtparser.parsers import GemfileParser


GEMFILE = """
# Example Gemfile
source 'https://rubygems.org'

ruby '2.0.0'

gem 'rails', '4.0.0'
gem 'rails-i18n', '~> 4.0.0.pre'
gem 'mysql2'
gem 'yajl-ruby', require: 'yajl'

group :production do
  gem 'unicorn'
  gem 'exception_notification', github: 'smartinez87/exception_notification'
end
"""


class BaseTestCase(TestCase):
    def setUp(self):
        super(BaseTestCase, self).setUp()
        self.parser = GemfileParser()


class GemfileDetectTestCase(BaseTestCase):
    def test_gemfile(self):
        self.assertTrue(self.parser.detect(GEMFILE))

    def test_unknown(self):
        content = "#include <iostream>"
        self.assertFalse(self.parser.detect(content))


class GemfileParseTestCase(BaseTestCase):
    maxDiff = None

    def test_gemfile(self):
        expect = {
            'filename': self.parser.filename,
            'language': self.parser.language,
            'platform': None,
            'version':  '2.0.0',
            'packages': [
                {'name': 'rails',
                 'version': '4.0.0',
                 'version_special': ''},
                {'name': 'rails-i18n',
                 'version': '4.0.0.pre',
                 'version_special': '~>'},
                {'name': 'mysql2',
                 'version': None,
                 'version_special': 'stable'},
                {'name': 'yajl-ruby',
                 'version': None,
                 'version_special': 'stable'},
                {'name': 'unicorn',
                 'version': None,
                 'version_special': 'stable'},
                {'name': 'exception_notification',
                 'version': None,
                 'version_special': 'latest'},
            ],
        }
        self.assertEqual(self.parser.parse(GEMFILE), expect)
