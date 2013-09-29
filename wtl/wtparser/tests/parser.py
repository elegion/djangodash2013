from __future__ import unicode_literals

from django.test import TestCase

from wtl.wtparser.parser import parse, guess, load, get_parser_for_filename
from wtl.wtparser.parsers import RequirementsParser, GemfileParser, PodfileParser
from wtl.wtparser.tests.parsers.gemfile import GEMFILE
from wtl.wtparser.tests.parsers.podfile import PODFILE
from wtl.wtparser.tests.parsers.requirements_txt import REQUIREMENTS


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


class GetParserForFilenameTestCase(TestCase):
    def test_requiremets(self):
        self.assertEqual(get_parser_for_filename('requirements.txt').__class__,
                         RequirementsParser)

    def test_gemfile(self):
        self.assertEqual(get_parser_for_filename('Gemfile').__class__,
                         GemfileParser)

    def test_podfile(self):
        self.assertEqual(get_parser_for_filename('Podfile').__class__,
                         PodfileParser)

    def test_unknown(self):
        self.assertIsNone(get_parser_for_filename('unknown'))
