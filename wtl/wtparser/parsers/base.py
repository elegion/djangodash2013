from __future__ import unicode_literals

import re
from itertools import repeat


class BaseParser(object):
    language = 'unknown'
    filename = 'unknown'

    def detect(self, content):
        return False

    def _detect_by_regex(self, content, pats):
        return any(re.compile(p, re.MULTILINE).search(content) for p in pats)

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
        return [l.strip() for l in lines if l.strip().startswith(init)]

    def _get_line_match_group(self, lines, group, regex):
        return self._get_match(lines[0], group, regex) if len(lines) else None

    def _get_match(self, line, group, regex):
        ms = re.compile(regex).match(line)
        if ms is not None:
            return ms.groupdict().get(group, None)

    def _get_match_groups(self, line, regex):
        ms = re.compile(regex).match(line)
        return ms.groups() if ms is not None else repeat(None)
