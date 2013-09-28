from __future__ import unicode_literals

from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _

from wtl.wtgithub.models import Repository as GithubRepository


@python_2_unicode_compatible
class Library(models.Model):
    """
    Library.

    This is what all this is about.
    """
    name = models.CharField(_('name'), max_length=512,
                            null=False, blank=False)
    url_home = models.URLField(_('homepage URL'), max_length=1024,
                               null=False, blank=True, default='')
    url_docs = models.URLField(_('documentation URL'), max_length=1024,
                               null=False, blank=True, default='')
    url_repo = models.URLField(_('repository URL'), max_length=1024,
                               null=False, blank=True, default='')
    github = models.OneToOneField(GithubRepository, related_name='library',
                                  verbose_name=_('github'), blank=True,
                                  null=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    total_users = models.BigIntegerField(_('total number of users'),
                                         null=False, blank=True, default=0,
                                         editable=False)

    class Meta():
        ordering = ('name',)

    def __str__(self):
        return self.name


@python_2_unicode_compatible
class LibraryVersion(models.Model):
    """
    Library Versions.

    A library may have many versions. We need to keep that in mind, and in the
    database!
    """
    library = models.ForeignKey(Library)
    version = models.CharField(_('version'), max_length=128,
                               null=False, blank=False)
    total_users = models.BigIntegerField(_('total number of users'),
                                         null=False, blank=True, default=0,
                                         editable=False)

    def __str__(self):
        return '%s %s' % (self.library.name, self.version)


@python_2_unicode_compatible
class Project(models.Model):
    """
    Project

    Contains information about projects using libraries.
    """
    name = models.CharField(_('name'), max_length=512,
                            null=False, blank=False)
    github = models.OneToOneField(GithubRepository, related_name='project',
                                  verbose_name=_('github'), blank=True,
                                  null=True)
    libraries = models.ManyToManyField(Library, through='ProjectLibrary',
                                       verbose_name=_('libraries'))


@python_2_unicode_compatible
class ProjectLibrary(models.Model):
    """
    ProjectLibrary

    Contains information about Libraries used by Projects (current and old)
    """
    project = models.ForeignKey(Project)
    library = models.ForeignKey(Library)
    libraryVersion = models.ForeignKey(LibraryVersion)
    added_on = models.DateTimeField()
    removed_on = models.DateTimeField(blank=True, null=True)
