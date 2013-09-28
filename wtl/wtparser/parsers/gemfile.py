from __future__ import unicode_literals

import re

from .base import BaseParser


class GemfileParser(BaseParser):
    filetype = 'gemfile'

    def detect(self, content):
        res = [
            r'''^\s*source\s+["']https://rubygems.org['"]''',
            r'''^\s*ruby\s+["'].*['"]''',
            r'''^\s*group.+do''',
            r'''^\s*gem\s+["'].*['"]''',
        ]
        return any(re.compile(r).match(content) for r in res)
