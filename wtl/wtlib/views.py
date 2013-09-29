from __future__ import unicode_literals

from django.shortcuts import render, redirect

from wtl.wtlib.forms import AnalyzeForm


def home(request):
    if request.method == 'POST':
        form = AnalyzeForm(request.POST)
        if form.is_valid() and form.analyze():
            return redirect(form.project)
    else:
        form = AnalyzeForm()
    return render(request, 'wtlib/home.html', {'analyze_form': form})


def project(request, project_id):
    return render(request, 'wtlib/project.html')
