from currency.models import Source

from django import forms


class SourceForm(forms.ModelForm):
    class Meta:
        model = Source
        fields = ('source_url', 'name')
