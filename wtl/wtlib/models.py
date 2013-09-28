from __future__ import print_function
from __future__ import unicode_literals

from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _


@python_2_unicode_compatible
class Library(models.Model):
    """
    Library.

    This is what all this is about.
    """
    name = models.CharField(_('name'), max_length=512)
    url_home = models.URLField(_('homepage URL'), max_length=1024)
    url_docs = models.URLField(_('documentation URL'), max_length=1024)
    url_repo = models.URLField(_('repository URL'), max_length=1024)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    total_users = models.BigIntegerField(_('total number of users'),
                                         null=False, blank=True, default=0,
                                         editable=False)

    class Meta():
        ordering = ('name',)

    def __str__(self):
        return self.name
