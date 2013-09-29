from __future__ import unicode_literals
from django.core.urlresolvers import reverse

from autoslug import AutoSlugField
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _

from wtl.wtgithub.models import Repository as GithubRepository


@python_2_unicode_compatible
class Language(models.Model):
    """
    Language

    A language. Programming language.
    """
    name = models.CharField(_('name'), max_length=128,
                            null=False, blank=False)
    slug = AutoSlugField(populate_from='name', unique=True)
    url_home = models.URLField(_('homepage URL'), max_length=1024,
                               null=False, blank=True, default='')
    color = models.CharField(_('color'), max_length=32, null=False, blank=True,
                             default="#ffffff")
    total_users = models.BigIntegerField(_('total number of users'),
                                         null=False, blank=True, default=0,
                                         editable=False, db_index=True)

    class Meta():
        ordering = ('-total_users',)
        verbose_name = _('language')
        verbose_name_plural = _('languages')

    def __str__(self):
        return self.name

    @classmethod
    def update_totals(cls):
        languages = cls.objects.annotate(count=models.Count('library'))
        for l in languages:
            l.total_users = l.count or 0
            l.save(update_fields=['total_users'])


@python_2_unicode_compatible
class Library(models.Model):
    """
    Library

    This is what all this is about.
    """
    language = models.ForeignKey(Language, verbose_name=_('language'),
                                 null=False, blank=False)
    name = models.CharField(_('name'), max_length=512,
                            null=False, blank=False)
    slug = AutoSlugField(populate_from='name', unique=True)
    short_description = models.TextField()
    license = models.TextField()
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

    @classmethod
    def update_totals_by_project(cls, project):
        # Not the best solution, but both my brain right now and Django ORM are
        # limited in their abilities.
        libs = cls.objects \
            .filter(id__in=project.libraries.all) \
            .annotate(count=models.Sum('versions__total_users'))
        for l in libs:
            l.total_users = l.count or 0
            l.save(update_fields=['total_users'])
        Language.update_totals()

    def get_absolute_url(self):
        return reverse('wtlib_library', args=[self.slug])


@python_2_unicode_compatible
class LibraryVersion(models.Model):
    """
    Library Versions

    A library may have many versions. We need to keep that in mind, and in the
    database!
    """
    library = models.ForeignKey(Library, related_name='versions')
    version = models.CharField(_('version'), max_length=128,
                               null=True, blank=True)
    version_special = models.CharField(_('version special'), max_length=128,
                                       null=True, blank=True)
    release_date = models.DateField(null=True, blank=True, db_index=True)
    total_users = models.BigIntegerField(_('total number of users'),
                                         null=False, blank=True, default=0,
                                         editable=False)

    class Meta():
        ordering = ('-release_date',)
        verbose_name = _('library version')
        verbose_name_plural = _('library versions')

    def __str__(self):
        return '{0} {1}'.format(self.library.name, self.version)

    @classmethod
    def update_totals_by_project(cls, project):
        # Not the best solution, but both my brain right now and Django ORM are
        # limited in their abilities.
        versions = cls.objects \
            .filter(id__in=project.libraries.all) \
            .annotate(count=models.Count('projects'))
        for v in versions:
            v.total_users = v.count or 0
            v.save(update_fields=['total_users'])
        Library.update_totals_by_project(project)


@python_2_unicode_compatible
class Project(models.Model):
    """
    Project

    Contains information about projects using libraries.
    """
    name = models.CharField(_('name'), max_length=512,
                            null=False, blank=False)
    slug = AutoSlugField(populate_from='name', unique=True)
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
        return reverse('wtlib_project', args=[self.slug])
