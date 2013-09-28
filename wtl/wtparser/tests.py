from __future__ import unicode_literals

from django.test import TestCase

from .parser import guess
from .parsers import RequirementsParser, GemfileParser, PodfileParser


class GuessTestCase(TestCase):
    def test_requirements(self):
        with open('requirements.txt', 'r') as f:
            content = f.read()
        self.assertEqual(guess(content).__class__, RequirementsParser)

    def test_gemfile(self):
        content = """
        source 'https://rubygems.org'
        gem 'rails', '4.0'
        """
        self.assertEqual(guess(content).__class__, GemfileParser)

    def test_podfile(self):
        content = """
        platform :ios
        pod 'SSToolkit'
        """
        self.assertEqual(guess(content).__class__, PodfileParser)

    def test_unknown(self):
        content = "#include <iostream>"
        with self.assertRaises(AttributeError):
            guess(content)
