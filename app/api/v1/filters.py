from currency.models import ContactUs, Rate, Source

import django_filters


class RateFilter(django_filters.FilterSet):
    class Meta:
        model = Rate
        fields = {
            'source': ('exact',),
            'type': ('exact',),
            'base_type': ('exact',),
            'buy': ('gte', 'lte'),
            'sale': ('gte', 'lte'),
        }


class SourceFilter(django_filters.FilterSet):
    class Meta:
        model = Source
        fields = {
            'name': ('exact',),
            'source_url': ('exact',),
        }


class ContactUsFilter(django_filters.FilterSet):
    class Meta:
        model = ContactUs
        fields = {
            'created': ('gte', 'lte'),
            'email_from': ('exact',),
            'reply_to': ('exact',),
        }
