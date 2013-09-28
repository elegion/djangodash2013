from __future__ import unicode_literals

import factory
from . import models


class LibraryFactory(factory.Factory):
    FACTORY_FOR = models.Library
    name = 'mylib'
