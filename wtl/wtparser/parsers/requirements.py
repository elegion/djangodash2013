from __future__ import unicode_literals

import re

from base import BaseParser


class RequirementsParser(BaseParser):
    filetype = 'requirements'

    def detect(self, content):
        res = [
            r'''^--index-url ''',
            r'''^-i ''',
            r'''^--no-index$''',
            r'''^--extra-index-url''',
            r'''^--find-links ''',
            r'''^-f ''',
            r'''^-r ''',
            r'''^-e ''',
            r'''^.*(==|>=)''',
        ]
        return any(re.compile(r).match(content) for r in res)
