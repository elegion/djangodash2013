from __future__ import unicode_literals

import requirements

from wtl.wtparser.parsers.base import BaseParser


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
            r'''^\w.*[=<>]+''',
        ]
        return self._detect_by_regex(content, res)

    def get_packages(self, lines):
        reqs = requirements.parse('\n'.join(lines))
        return [self._get_req(r) for r in reqs if not r.local_file]

    def _get_req(self, req):
        if len(req.specs) > 0 and not req.vcs:
            version = req.specs[0][1]
            special = req.specs[0][0] if req.specs[0][0] != '==' else ''
        elif len(req.specs) == 0 and not req.vcs:
            version = None
            special = 'stable'
        elif req.vcs:
            version = None
            special = 'latest'
        return {'name': req.name,
                'version': version,
                'version_special': special}
