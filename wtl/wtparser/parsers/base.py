from __future__ import unicode_literals

import re


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
