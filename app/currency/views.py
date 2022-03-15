from currency.models import ContactUs, Rate

from django.shortcuts import render


def contacts_list(request):
    contacts = ContactUs.objects.all()
    return render(request, 'contact_us.html', context={'contacts_list': contacts})


def rate_list(request):
    rate = Rate.objects.all()
    return render(request, 'rate.html', context={'rate_list': rate})


def index(request):
    return render(request, 'index.html')
