from currency.models import ContactUs

from django.http import HttpResponse


def contacts_list(request):
    contacts = []
    for contact in ContactUs.objects.all():
        contacts.append([contact.id, contact.email_from, contact.subject, contact.message, contact.created])
    return HttpResponse(str(contacts))
