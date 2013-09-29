from __future__ import unicode_literals

from . import parsers


__all__ = ['parse', 'get_parser_for_filename']


def parse(content, filetype=None):
    """
    Parse the packages file and return the data in the following format::

        {
            'filename': 'Gemfile',
            'language': 'Objective-C',
            'platform': 'ios',
            'version':  '7.0',
            'packages': [
                {
                    'name': 'Django',
                    'version': '1.7',
                },
            ]
        }

    :param content: the package file contents
    :param filetype: the package file type, for example `requirements`,
        `gemfile`, `podfile`. May be `None` to ask the parser to detect the
        type automatically.
    """
    parser = guess(content) if filetype is None else load(filetype)
    return parser.parse(content)


def get_parser_for_filename(filename):
    for name in parsers.available_parsers:
        parser = load_by_name(name)()
        if parser.filename == filename:
            return parser
    return None


def guess(content):
    for name in parsers.available_parsers:
        parser = load_by_name(name)()
        if parser.detect(content):
            return parser
    raise AttributeError('No parser for this file.')


def load(filetype):
    return load_by_name('{0}Parser'.format(filetype.capitalize()))()


def load_by_name(name):
    return getattr(parsers, name)
