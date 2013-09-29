from django import forms

from wtl.wtgithub.worker import GithubWorker


class AnalyzeForm(forms.Form):
    git_url = forms.CharField()

    def analyze(self):
        worker = GithubWorker()
        self.repository, self.project = worker.analyze_repo(self.cleaned_data['git_url'])
        return self.repository, self.project
