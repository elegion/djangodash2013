from django import forms


class AnalyzeForm(forms.Form):
    git_url = forms.CharField()
