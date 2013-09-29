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

PODFILE = """
# Example Podfile
platform :ios, '7.0'
inhibit_all_warnings!

xcodeproj `MyProject`

pod 'SSToolkit'
pod 'AFNetworking', '>= 0.5.1'
pod 'Objection', :head # 'bleeding edge'
pod 'Rejection', '0.0.0'

target :test do
  pod 'OCMock', '~> 2.0.1'
end

generate_bridge_support!

post_install do |installer|
  installer.project.targets.each do |target|
    puts "#target.name"
  end
end
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
