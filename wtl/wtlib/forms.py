from django import forms
from django.forms.util import ErrorList
from django.utils.translation import ugettext_lazy as _
from github import UnknownObjectException

from wtl.wtgithub.worker import GithubWorker, ParseError


class AnalyzeForm(forms.Form):
    git_url = forms.CharField()

    def analyze(self):
        if 'git_url' not in self._errors:
            self._errors['git_url'] = ErrorList()
        worker = GithubWorker()
        try:
            self.repository, self.project = worker.analyze_repo(
                self.cleaned_data['git_url'])
            return self.repository, self.project
        except UnknownObjectException:
            self._errors['git_url'].append(_('Repository not found.'))
        except ParseError:
            self._errors['git_url'].append(_('Failed to parse your repo.'))
