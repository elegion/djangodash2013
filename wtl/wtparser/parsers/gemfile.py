from __future__ import unicode_literals

from .base import BaseParser
from .regex import RegexParserMixin


class GemfileParser(BaseParser, RegexParserMixin):
    language = 'Ruby'
    filename = 'Gemfile'

    def detect(self, content):
        res = [
            r'''^\s*source\s+["']https://rubygems.org['"]''',
            r'''^\s*ruby\s+["'].*['"]''',
            r'''^\s*group.+do''',
            r'''^\s*gem\s+["'].*['"]''',
        ]
        return self._detect_by_regex(content, res)

    def get_version(self, lines):
        return self._get_value(
            lines, 'ruby', r'^ruby\s+(?P<quot>"|\')(?P<x>.+)(?P=quot).*$')

    def get_packages(self, lines):
        return [self._gem(l) for l in self._lines_startwith(lines, 'gem ')]

    def _gem(self, line):
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
                version_string = self._match(rest, 'x', self.quoted_re)
                if version_string is None:
                    version = None
                    special = 'stable'
                else:
                    special, version = self._match_groups(version_string,
                                                          self.version_re)

        name = self._match(name_arg, 'x', self.quoted_re)
        return {'name': name,
                'version': version,
                'version_special': special}
