from __future__ import unicode_literals


def parse(content, filetype=None):
    """
    Parse the packages file and return the data in the following format::

        {
            'language': 'python',
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
    pass
