from api.serializers import ContactUsSerializer, RateSerializer, SourceSerializer

from currency.models import ContactUs, Rate, Source

from rest_framework import generics, viewsets
from rest_framework.renderers import JSONRenderer

from rest_framework_csv.renderers import CSVRenderer

from rest_framework_xml.renderers import XMLRenderer


class RateViewSet(viewsets.ModelViewSet):
    queryset = Rate.objects.all()
    serializer_class = RateSerializer
    renderer_classes = (JSONRenderer, XMLRenderer, CSVRenderer)


class SourceListView(generics.ListCreateAPIView):
    queryset = Source.objects.all()
    serializer_class = SourceSerializer


class ContactsViewSet(viewsets.ModelViewSet):
    queryset = ContactUs.objects.all()
    serializer_class = ContactUsSerializer
    renderer_classes = (JSONRenderer, XMLRenderer, CSVRenderer)
