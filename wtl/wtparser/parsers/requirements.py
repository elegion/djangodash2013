from __future__ import unicode_literals

from .base import BaseParser


class RequirementsParser(BaseParser):
    language = 'Python'
    filename = 'requirements.txt'

    def detect(self, content):
        res = [
            r'''^--index-url ''',
            r'''^-i ''',
            r'''^--no-index''',
            r'''^--extra-index-url ''',
            r'''^--find-links ''',
            r'''^-f ''',
            r'''^-r ''',
            r'''^-e ''',
            r'''^.*(==|>=)''',
        ]
        return self._detect_by_regex(content, res)
