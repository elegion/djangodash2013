from __future__ import unicode_literals

from django.test import TestCase

from wtl.wtparser.parsers import PodfileParser


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
        self.parser = PodfileParser()


class PodfileDetectTestCase(BaseTestCase):
    def test_podfile(self):
        self.assertTrue(self.parser.detect(PODFILE))

    def test_unknown(self):
        content = "#include <iostream>"
        self.assertFalse(self.parser.detect(content))


class PodfileParseTestCase(BaseTestCase):
    maxDiff = None

    def test_podfile(self):
        expect = {
            'filename': self.parser.filename,
            'language': self.parser.language,
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
        self.assertEqual(self.parser.parse(PODFILE), expect)
