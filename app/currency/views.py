from currency.forms import SourceForm
from currency.models import ContactUs, Rate, Source

from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView


class ContactUsList(ListView):
    queryset = ContactUs.objects.all()
    template_name = 'contact_us.html'


class RateList(ListView):
    queryset = Rate.objects.all()
    template_name = 'rate.html'


class SourceList(ListView):
    queryset = Source.objects.all().order_by('-id')
    template_name = 'source.html'


class SourceCreate(CreateView):
    model = Source
    template_name = 'source_create.html'
    form_class = SourceForm
    success_url = reverse_lazy('currency:source_list')


class SourceUpdate(UpdateView):
    model = Source
    template_name = 'source_update.html'
    form_class = SourceForm
    success_url = reverse_lazy('currency:source_list')


class SourceDelete(DeleteView):
    model = Source
    template_name = 'source_delete.html'
    success_url = reverse_lazy('currency:source_list')


class SourceDetail(DetailView):
    model = Source
    template_name = 'source_detail.html'
