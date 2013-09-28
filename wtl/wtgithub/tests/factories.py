from __future__ import unicode_literals

import factory
from wtl.wtgithub import models


class RepositoryFactory(factory.DjangoModelFactory):
    FACTORY_FOR = models.Repository

    name = 'myproj'
    owner = 'me'
    starsCount = 0
    description = 'my project'
