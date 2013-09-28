from __future__ import unicode_literals

from django.test import TestCase

from .parser import parse, guess, load
from .parsers import RequirementsParser, GemfileParser, PodfileParser


with open('requirements.txt', 'r') as f:
    REQUIREMENTS = f.read()

GEMFILE = """
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


class GuessTestCase(TestCase):
    def test_requirements(self):
        self.assertEqual(guess(REQUIREMENTS).__class__, RequirementsParser)

    def test_gemfile(self):
        self.assertEqual(guess(GEMFILE).__class__, GemfileParser)

    def test_podfile(self):
        self.assertEqual(guess(PODFILE).__class__, PodfileParser)

    def test_unknown(self):
        content = "#include <iostream>"
        with self.assertRaises(AttributeError):
            guess(content)


class LoadTestCase(TestCase):
    def test_requirements(self):
        self.assertEqual(load('requirements').__class__, RequirementsParser)

    def test_gemfile(self):
        self.assertEqual(load('gemfile').__class__, GemfileParser)

    def test_podfile(self):
        self.assertEqual(load('podfile').__class__, PodfileParser)

    def test_unknown(self):
        with self.assertRaises(AttributeError):
            load('unknown')


class ParseTestCase(TestCase):
    maxDiff = None

    def test_podfile(self):
        parser = PodfileParser()
        expect = {
            'filename': parser.filename,
            'language': parser.language,
            'platform': 'ios',
            'version':  '7.0',
            'packages': [
                {'name': 'SSToolkit',
                 'version': None,
                 'version_special': 'stable'},
                {'name': 'AFNetworking',
                 'version': '0.5.1',
                 'version_special': '>='},
                {'name': 'Objection',
                 'version': None,
                 'version_special': 'latest'},
                {'name': 'Rejection',
                 'version': '0.0.0',
                 'version_special': ''},
                {'name': 'OCMock',
                 'version': '2.0.1',
                 'version_special': '~>'},
            ],
        }
        self.assertEqual(parser.parse(PODFILE), expect)

    def test_gemfile(self):
        parser = GemfileParser()
        expect = {
            'filename': parser.filename,
            'language': parser.language,
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
        self.assertEqual(parser.parse(GEMFILE), expect)

    def test_requirements(self):
        parser = RequirementsParser()
        expect = {
            'filename': parser.filename,
            'language': parser.language,
            'platform': None,
            'version':  None,
            'packages': None,
        }
        self.assertEqual(parser.parse(REQUIREMENTS), expect)
