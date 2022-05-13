from api.v1.filters import ContactUsFilter, RateFilter, SourceFilter
from api.v1.pagination import RatesPagination
from api.v1.serializers import ContactUsSerializer, RateSerializer, SourceSerializer
from api.v1.throttles import AnonCurrencyThrottle

from currency.models import ContactUs, Rate, Source

from django_filters import rest_framework as filters

from rest_framework import filters as rest_framework_filters
from rest_framework import generics, viewsets
from rest_framework.renderers import JSONRenderer

from rest_framework_csv.renderers import CSVRenderer

from rest_framework_xml.renderers import XMLRenderer


class RateViewSet(viewsets.ModelViewSet):
    queryset = Rate.objects.all()
    serializer_class = RateSerializer
    renderer_classes = (JSONRenderer, XMLRenderer, CSVRenderer)
    pagination_class = RatesPagination
    filterset_class = RateFilter
    filter_backends = (
        filters.DjangoFilterBackend,
        rest_framework_filters.OrderingFilter,
    )
    ordering_fields = ('id', 'sale', 'buy')
    throttle_classes = [AnonCurrencyThrottle]


class SourceListView(generics.ListCreateAPIView):
    queryset = Source.objects.all()
    serializer_class = SourceSerializer
    filterset_class = SourceFilter
    filter_backends = (
        filters.DjangoFilterBackend,
        rest_framework_filters.OrderingFilter,
    )
    ordering_fields = ('id', 'name', 'source_url')


class ContactsViewSet(viewsets.ModelViewSet):
    queryset = ContactUs.objects.all()
    serializer_class = ContactUsSerializer
    renderer_classes = (JSONRenderer, XMLRenderer, CSVRenderer)
    filterset_class = ContactUsFilter
    filter_backends = (
        filters.DjangoFilterBackend,
        rest_framework_filters.OrderingFilter,
        rest_framework_filters.SearchFilter,
    )
    ordering_fields = ('id', 'created', 'email_from', 'reply_to')
    search_fields = ['email_from', 'subject', 'message']
