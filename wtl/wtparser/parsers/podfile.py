from __future__ import unicode_literals

from .base import BaseParser


class PodfileParser(BaseParser):
    language = 'Objective-C'
    filename = 'Podfile'

    def detect(self, content):
        res = [
            r'''^\s*platform\s+(:ios|:osx)''',
            r'''^\s*xcodeproj\s+`.+`''',
            r'''^\s*target.+do''',
            r'''^\s*post_install\s+do''',
            r'''^\s*pod\s+["'].*['"]''',
        ]
        return self._detect_by_regex(content, res)

    def get_platform(self, lines):
        platform = self._get_platform(lines)
        r = r'''^platform\s+:(?P<name>\w+)(\s|,|#|$)'''
        return self._get_line_match_group(platform, 'name', r)

    def get_version(self, lines):
        platform = self._get_platform(lines)
        r = r'''^platform\s+:\w+\s*,\s*(?P<quot>"|')(?P<ver>.+)(?P=quot)'''
        return self._get_line_match_group(platform, 'ver', r)

    def get_packages(self, lines):
        return [self._get_pod(p) for p in self._get_pods(lines)]

    def _get_platform(self, lines):
        return self._get_lines_startswith(lines, 'platform ')

    def _get_pods(self, lines):
        return self._get_lines_startswith(lines, 'pod ')

    def _get_pod(self, line):
        quoted_re = r'''(?P<q>"|')(?P<x>.+)(?P=q)'''
        version_re = r'''(?P<s>[<>=~]*)\s*(?P<n>.*)'''

        args = line[4:].lstrip()
        if ',' not in args:
            name_arg = args
            version = None
            special = 'stable'
        else:
            name_arg, _, rest = [x.strip() for x in args.partition(',')]
            if rest.startswith(':head'):
                version = None
                special = 'latest'
            else:
                version_string = self._get_match(rest, 'x', quoted_re)
                special, version = self._get_match_groups(version_string,
                                                          version_re)

        name = self._get_match(name_arg, 'x', quoted_re)
        return {'name': name,
                'version': version,
                'version_special': special}
