from __future__ import unicode_literals

import re

from .base import BaseParser


class GemfileParser(BaseParser):
    language = 'Ruby'
    filename = 'Gemfile'

    def detect(self, content):
        res = [
            r'''^\s*source\s+["']https://rubygems.org['"]''',
            r'''^\s*ruby\s+["'].*['"]''',
            r'''^\s*group.+do''',
            r'''^\s*gem\s+["'].*['"]''',
        ]
        return any(re.compile(r).match(content) for r in res)

    def get_version(self, lines):
        ruby = self._get_ruby(lines)
        r = r'''^ruby\s+(?P<quot>"|')(?P<ver>.+)(?P=quot).*$'''
        return self._get_line_match_group(ruby, 'ver', r)

    def get_packages(self, lines):
        gems = self._get_gems(lines)
        return []

    def _get_ruby(self, lines):
        return self._get_lines_startswith(lines, 'ruby ')

    def _get_gems(self, lines):
        return self._get_lines_startswith(lines, 'gem ')
