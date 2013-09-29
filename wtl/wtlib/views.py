from __future__ import unicode_literals

from django.shortcuts import render, redirect, get_object_or_404

from wtl.wtcore.utils import paginate
from wtl.wtlib.forms import AnalyzeForm
from wtl.wtlib.models import Language, Project, Library


def home(request):
    if request.method == 'POST':
        form = AnalyzeForm(request.POST)
        if form.is_valid() and form.analyze():
            return redirect(form.project)
    else:
        form = AnalyzeForm()
    top_languages = Language.objects.filter(total_users__gt=0)[:3]
    return render(request, 'wtlib/home.html',
                  {'analyze_form': form,
                   'top_languages': top_languages})


def libraries_list(request, language_slug):
    libs = Library.objects.all()
    language = None
    if language_slug:
        language = get_object_or_404(Language, slug=language_slug)
        libs = libs.filter(language__slug=language_slug)
    libs = paginate(libs, 16, request.GET.get('page'))
    return render(request, 'wtlib/libraries_list.html',
                  {'libraries': libs,
                   'mixed_languages': language_slug is None,
                   'language': language,
                   'active_menu': 'libraries',
                   'active_language': language_slug})


def library(request, language_slug, library_slug):
    lib = get_object_or_404(Library, slug=library_slug)
    return render(request, 'wtlib/library.html',
                  {'library': lib,
                   'active_menu': 'libraries',
                   'active_language': language_slug})


def projects_list(request, language_slug):
    projects = Project.objects.all()
    language = None
    if language_slug:
        language = get_object_or_404(Language, slug=language_slug)
        projects = projects.filter(pk__in=Project.objects.filter(
            libraries__library__language__slug=language_slug))
    return render(request, 'wtlib/projects_list.html',
                  {'projects': projects,
                   'mixed_languages': language_slug is None,
                   'language': language,
                   'active_menu': 'projects',
                   'active_language': language_slug})


def project(request, language_slug, project_slug):
    project = get_object_or_404(Project, slug=project_slug)
    return render(request, 'wtlib/project.html',
                  {'project': project,
                   'active_menu': 'projects',
                   'active_language': language_slug})
