from __future__ import unicode_literals

import factory

from . import models


class LanguageFactory(factory.DjangoModelFactory):
    FACTORY_FOR = models.Language
    name = factory.Sequence(lambda n: 'lang {0}'.format(n))


class LibraryFactory(factory.DjangoModelFactory):
    FACTORY_FOR = models.Library
    language = factory.SubFactory(LanguageFactory)
    name = 'mylib'


class LibraryVersionFactory(factory.DjangoModelFactory):
    FACTORY_FOR = models.LibraryVersion
    library = factory.SubFactory(LibraryFactory)
    version = '0.1.0-alpha'


class ProjectFactory(factory.DjangoModelFactory):
    FACTORY_FOR = models.Project
