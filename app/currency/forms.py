from currency.models import ContactUs, Source

from django import forms


class SourceForm(forms.ModelForm):
    class Meta:
        model = Source
        fields = ('source_url', 'name')


class ContactusForm(forms.ModelForm):
    class Meta:
        model = ContactUs
        fields = ('email_from', 'reply_to', 'subject', 'message')
