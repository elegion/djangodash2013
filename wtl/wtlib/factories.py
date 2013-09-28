from __future__ import unicode_literals

import factory
from . import models


class LibraryFactory(factory.DjangoModelFactory):
    FACTORY_FOR = models.Library
    name = 'mylib'


class LibraryVersionFactory(factory.DjangoModelFactory):
    FACTORY_FOR = models.LibraryVersion
    library = factory.SubFactory(LibraryFactory)
    version = '0.1.0-alpha'
