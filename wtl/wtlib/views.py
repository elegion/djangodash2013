from __future__ import unicode_literals

from django.shortcuts import render, redirect, get_object_or_404

from wtl.wtlib.forms import AnalyzeForm
from wtl.wtlib.models import Project, Library


def home(request):
    if request.method == 'POST':
        form = AnalyzeForm(request.POST)
        if form.is_valid() and form.analyze():
            return redirect(form.project)
    else:
        form = AnalyzeForm()
    return render(request, 'wtlib/home.html', {'analyze_form': form})


def libraries_list(request):
    libs = Library.objects.all()
    return render(request, 'wtlib/libraries_list.html', {'libraries': libs})


def library(request, library_slug):
    lib = get_object_or_404(Library, slug=library_slug)
    return render(request, 'wtlib/library.html', {'library': lib})


def projects_list(request):
    projects = Project.objects.all()
    return render(request, 'wtlib/projects_list.html', {'projects': projects})


def project(request, project_slug):
    project = get_object_or_404(Project, slug=project_slug)
    return render(request, 'wtlib/project.html', {'project': project})
