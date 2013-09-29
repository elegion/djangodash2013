from __future__ import unicode_literals

from django.shortcuts import render

from wtl.wtlib.forms import AnalyzeForm


def home(request):
    if request.method == 'POST':
        form = AnalyzeForm(request.POST)
    else:
        form = AnalyzeForm()
    return render(request, 'wtlib/home.html', {'analyze_form': form})
