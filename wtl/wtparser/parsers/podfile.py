from __future__ import unicode_literals

import re

from .base import BaseParser


class PodfileParser(BaseParser):
    language = 'Objective-C'
    filename = 'Podfile'

    def detect(self, content):
        res = [
            r'''^\s*platform\s+(:ios|:osx)''',
            r'''^\s*xcodeproj\s+`.+`''',
            r'''^\s*target.+do''',
            r'''^\s*post_install\s+do''',
            r'''^\s*pod\s+["'].*['"]''',
        ]
        return any(re.compile(r).match(content) for r in res)

    def get_platform(self, lines):
        platform = self._get_platform(lines)
        r = r'''^platform\s+:(?P<name>\w+)(\s|,|#|$)'''
        return self._get_match_group(platform, 'name', r)

    def get_version(self, lines):
        platform = self._get_platform(lines)
        r = r'''^platform\s+:\w+\s*,\s*(?P<quot>"|')(?P<ver>.+)(?P=quot)'''
        return self._get_match_group(platform, 'ver', r)

    def get_packages(self, lines):
        pods = self._get_pods(lines)
        return []

    def _get_platform(self, lines):
        return self._get_lines_startswith(lines, 'platform ')

    def _get_pods(self, lines):
        return self._get_lines_startswith(lines, 'pod ')
