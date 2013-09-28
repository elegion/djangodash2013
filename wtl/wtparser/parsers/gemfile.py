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
        return [self._get_gem(l) for l in self._get_gems(lines)]

    def _get_ruby(self, lines):
        return self._get_lines_startswith(lines, 'ruby ')

    def _get_gems(self, lines):
        return self._get_lines_startswith(lines, 'gem ')

    def _get_gem(self, line):
        quoted_re = r'''(?P<q>"|')(?P<x>.+)(?P=q)'''
        version_re = r'''(?P<s>[<>=~]*)\s*(?P<n>.*)'''

        args = line[4:].lstrip()
        if ',' not in args:
            name_arg = args
            version = None
            special = 'stable'
        else:
            name_arg, _, rest = [x.strip() for x in args.partition(',')]
            if any(x in rest for x in [':git', 'git:', ':github', 'github:']):
                version = None
                special = 'latest'
            else:
                version_string = self._get_match(rest, 'x', quoted_re)
                if version_string is None:
                    version = None
                    special = 'stable'
                else:
                    special, version = self._get_match_groups(version_string,
                                                              version_re)

        name = self._get_match(name_arg, 'x', quoted_re)
        return {'name': name,
                'version': version,
                'version_special': special}
