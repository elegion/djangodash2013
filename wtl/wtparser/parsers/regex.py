import re
from itertools import repeat


class RegexParserMixin(object):
    quoted_re = r'''(?P<q>"|')(?P<x>.+)(?P=q)'''
    version_re = r'''(?P<s>[<>=~]*)\s*(?P<n>.*)'''

    def _get_value(self, lines, prefix, regex):
        filtered = self._lines_startwith(lines, '{0} '.format(prefix))
        return self._match(filtered[0], 'x', regex) if len(lines) else None

    def _lines_startwith(self, lines, init):
        return [l.strip() for l in lines if l.strip().startswith(init)]

    def _match(self, line, group, regex):
        ms = re.compile(regex).match(line)
        if ms is not None:
            return ms.groupdict().get(group, None)

    def _match_groups(self, line, regex):
        ms = re.compile(regex).match(line)
        return ms.groups() if ms is not None else repeat(None)
