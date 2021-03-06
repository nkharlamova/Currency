from currency.models import ContactUs, Rate, Source

from django import forms


class SourceForm(forms.ModelForm):
    class Meta:
        model = Source
        fields = ('source_url', 'name', 'code_name', 'logo')


class ContactusForm(forms.ModelForm):
    class Meta:
        model = ContactUs
        fields = ('email_from', 'reply_to', 'subject', 'message')


class RateForm(forms.ModelForm):
    class Meta:
        model = Rate
        fields = ('type', 'base_type', 'source', 'buy', 'sale')
