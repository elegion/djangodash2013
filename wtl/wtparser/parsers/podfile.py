from __future__ import unicode_literals

import re

from .base import BaseParser


class PodfileParser(BaseParser):
    filetype = 'podfile'

    def detect(self, content):
        res = [
            r'''^\s*platform\s+(:ios|:osx)''',
            r'''^\s*xcodeproj\s+`.+`''',
            r'''^\s*target.+do''',
            r'''^\s*post_install\s+do''',
            r'''^\s*pod\s+["'].*['"]''',
        ]
        return any(re.compile(r).match(content) for r in res)
