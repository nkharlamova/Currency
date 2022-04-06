from currency.forms import ContactusForm, RateForm, SourceForm
from currency.models import ContactUs, Rate, Source

from django.conf import settings
from django.contrib.auth.mixins import UserPassesTestMixin
from django.core.mail import send_mail
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView


class ContactUsList(ListView):
    queryset = ContactUs.objects.all()
    template_name = 'contact_us.html'


class RateList(ListView):
    queryset = Rate.objects.all().order_by('-id')
    template_name = 'rate.html'


class RateCreate(CreateView):
    model = Rate
    template_name = 'rate_create.html'
    form_class = RateForm
    success_url = reverse_lazy('currency:rate_list')


class RateUpdate(UserPassesTestMixin, UpdateView):
    model = Rate
    template_name = 'rate_update.html'
    form_class = RateForm
    success_url = reverse_lazy('currency:rate_list')

    def test_func(self):
        return self.request.user.is_superuser


class RateDelete(UserPassesTestMixin, DeleteView):
    model = Rate
    template_name = 'rate_delete.html'
    success_url = reverse_lazy('currency:rate_list')

    def test_func(self):
        return self.request.user.is_superuser


class RateDetail(DetailView):
    model = Rate
    template_name = 'rate_detail.html'


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


class ContactUsCreate(CreateView):
    model = ContactUs
    template_name = 'contactus_create.html'
    form_class = ContactusForm
    success_url = reverse_lazy('currency:contactus_list')

    def _send_email(self):
        recipient = settings.EMAIL_HOST_USER
        subject = 'User ContactUs'
        body = f'''
                Request From: {self.object.email_from}
                Email to reply: {self.object.reply_to}
                Subject: {self.object.subject}
                Body: {self.object.message}
                '''
        send_mail(
            subject,
            body,
            recipient,
            [recipient],
            fail_silently=False,
        )

    def form_valid(self, form):
        redirect = super().form_valid(form)
        self._send_email()
        return redirect

    def form_invalid(self, form):
        return super().form_invalid(form)
