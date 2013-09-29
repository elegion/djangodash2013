from django import forms
from django.forms.util import ErrorList
from django.utils.translation import ugettext_lazy as _
from github import UnknownObjectException

from wtl.wtgithub.worker import GithubWorker, ParseError, CantFindParserError


class AnalyzeForm(forms.Form):
    git_url = forms.CharField()

    def analyze(self):
        worker = GithubWorker()
        try:
            self.repository, self.project = worker.analyze_repo(
                self.cleaned_data['git_url'])
            return self.repository, self.project
        except UnknownObjectException:
            self._add_error('git_url', _('Repository not found.'))
        except CantFindParserError:
            self._add_error('git_url', _('Cant find requirements file..'))
        except ParseError:
            self._add_error('git_url', _('Failed to parse your repo.'))

    def _add_error(self, field, error):
        if field not in self._errors:
            self._errors[field] = ErrorList()
        self._errors[field].append(error)
