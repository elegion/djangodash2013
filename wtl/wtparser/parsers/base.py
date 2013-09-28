from __future__ import unicode_literals

import re
from operator import methodcaller


class BaseParser(object):
    language = 'unknown'
    filename = 'unknown'

    def detect(self, content):
        return False

    def get_platform(self, lines):
        return None

    def get_version(self, lines):
        return None

    def get_packages(self, lines):
        return None

    def parse(self, content):
        lines = content.splitlines()
        return {
            'filename': self.filename,
            'language': self.language,
            'platform': self.get_platform(lines),
            'version':  self.get_version(lines),
            'packages': self.get_packages(lines),
        }

    def _get_lines_startswith(self, lines, init):
        return filter(methodcaller('startswith', init),
                      map(methodcaller('strip'), lines))

    def _get_match_group(self, lines, group, regex):
        if len(lines) > 0:
            r = re.compile(regex)
            ms = r.match(lines[0])
            if ms is not None:
                return ms.groupdict().get(group, None)
        return None
