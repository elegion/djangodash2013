from __future__ import unicode_literals
from django.core.urlresolvers import reverse

from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _

from wtl.wtgithub.models import Repository as GithubRepository


@python_2_unicode_compatible
class Language(models.Model):
    """
    A language. Programming language.
    """
    name = models.CharField(_('name'), max_length=128,
                            null=False, blank=False)
    slug = models.SlugField(_('slug'), null=False, blank=False)
    url_home = models.URLField(_('homepage URL'), max_length=1024,
                               null=False, blank=True, default='')
    color = models.CharField(_('color'), max_length=32, null=False, blank=True,
                             default="#ffffff")

    def __str__(self):
        return self.name

    class Meta():
        verbose_name = _('language')
        verbose_name_plural = _('languages')


@python_2_unicode_compatible
class Library(models.Model):
    """
    Library.

    This is what all this is about.
    """
    language = models.ForeignKey(Language, verbose_name=_('language'),
                                 null=False, blank=False)
    name = models.CharField(_('name'), max_length=512,
                            null=False, blank=False)
    slug = models.SlugField(_('slug'), null=False, blank=False)
    url_home = models.URLField(_('homepage URL'), max_length=1024,
                               null=False, blank=True, default='')
    url_docs = models.URLField(_('documentation URL'), max_length=1024,
                               null=False, blank=True, default='')
    url_repo = models.URLField(_('repository URL'), max_length=1024,
                               null=False, blank=True, default='')
    github = models.OneToOneField(GithubRepository, related_name='library',
                                  verbose_name=_('github'), blank=True,
                                  null=True)
    total_users = models.BigIntegerField(_('total number of users'),
                                         null=False, blank=True, default=0,
                                         editable=False, db_index=True)

    class Meta():
        ordering = ('-total_users',)
        verbose_name = _('library')
        verbose_name_plural = _('libraries')

    def __str__(self):
        return self.name


@python_2_unicode_compatible
class LibraryVersion(models.Model):
    """
    Library Versions.

    A library may have many versions. We need to keep that in mind, and in the
    database!
    """
    library = models.ForeignKey(Library, related_name='versions')
    version = models.CharField(_('version'), max_length=128,
                               null=False, blank=False)
    release_date = models.DateField(null=True, blank=True, db_index=True)
    total_users = models.BigIntegerField(_('total number of users'),
                                         null=False, blank=True, default=0,
                                         editable=False)

    def __str__(self):
        return '%s %s' % (self.library.name, self.version)

    class Meta():
        ordering = ('-release_date',)
        verbose_name = _('library version')
        verbose_name_plural = _('library versions')


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
    libraries = models.ManyToManyField(LibraryVersion,
                                       verbose_name=_('libraries'),
                                       related_name='projects')

    class Meta():
        verbose_name = _('project')
        verbose_name_plural = _('projects')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('wtlib_project', args=[self.id])
