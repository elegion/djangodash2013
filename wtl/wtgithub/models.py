from __future__ import unicode_literals

from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _
from django.db import models


@python_2_unicode_compatible
class Repository(models.Model):
    """
    Repository

    Represents github repository. Name, description, etc
    """
    owner = models.CharField(_('owner'), max_length=512)
    name = models.CharField(_('name'), max_length=512)
    starsCount = models.IntegerField(_('stars count'))
    description = models.TextField(_('description'))
