from currency.forms import SourceForm
from currency.models import ContactUs, Rate, Source

from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render


def contacts_list(request):
    contacts = ContactUs.objects.all()
    return render(request, 'contact_us.html', context={'contacts_list': contacts})


def rate_list(request):
    rate = Rate.objects.all()
    return render(request, 'rate.html', context={'rate_list': rate})


def index(request):
    return render(request, 'index.html')


def source_list(request):
    source = Source.objects.all().order_by('-id')
    return render(request, 'source.html', context={'source_list': source})


def source_create(request):
    if request.method == 'POST':
        form = SourceForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/source-list/')
    else:
        form = SourceForm()
    return render(request, 'source_create.html', context={'form': form})


def source_update(request, pk):
    instance = get_object_or_404(Source, pk=pk)
    if request.method == 'POST':
        form = SourceForm(request.POST, instance=instance)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/source-list/')
    else:
        form = SourceForm(instance=instance)
    return render(request, 'source_update.html', context={'form': form})


def source_delete(request, pk):
    instance = get_object_or_404(Source, pk=pk)
    if request.method == 'POST':
        instance.delete()
        return HttpResponseRedirect('/source-list/')
    else:
        return render(request, 'source_delete.html', context={'source': instance})
