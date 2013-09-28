from __future__ import unicode_literals


class BaseParser(object):
    def detect(self, content):
        return False

    def parse(self, content):
        raise NotImplemented('Must override `parse` method.')
