from currency.models import ContactUs, Rate, Source

from django.urls import reverse

from rest_framework.test import APIClient


def test_rates_get_list():
    client = APIClient()
    response = client.get(reverse('api-v1:rate-list'))
    assert response.status_code == 200
    assert response.json()


def test_rates_post_empty_data():
    client = APIClient()
    response = client.post(reverse('api-v1:rate-list'), data={})
    assert response.status_code == 400
    assert response.json() == {
        'sale': ['This field is required.'],
        'buy': ['This field is required.'],
        'source': ['This field is required.'],
        'type': ['This field is required.'],
    }


def test_rates_post_valid_data():
    client = APIClient()
    source = Source.objects.last()
    payload = {
        'sale': 23,
        'buy': 24,
        'source': source.id,
        'type': 'USD'
    }
    response = client.post(reverse('api-v1:rate-list'), data=payload)
    assert response.status_code == 201
    assert response.json()


def test_rates_patch_valid_data():
    client = APIClient()
    rate = Rate.objects.last()
    payload = {
        'sale': 28,
    }
    response = client.patch(reverse('api-v1:rate-detail', args=[rate.id]), data=payload)
    assert response.status_code == 200
    assert response.json()['sale'] == '28.00'


def test_rates_delete():
    client = APIClient()
    rate = Rate.objects.last()

    response = client.delete(reverse('api-v1:rate-detail', args=[rate.id]))
    assert response.status_code == 204
    assert response.content == b''


def test_contactus_get_list():
    client = APIClient()
    response = client.get(reverse('api-v1:contact-list'))
    assert response.status_code == 200
    assert response.json


def test_contactus_post_empty_data():
    client = APIClient()
    response = client.post(reverse('api-v1:contact-list'), data={})
    assert response.status_code == 400
    assert response.json() == {
        'email_from': ['This field is required.'],
        'subject': ['This field is required.'],
        'message': ['This field is required.'],
    }


def test_contactus_post_valid_data():
    client = APIClient()
    payload = {
        'email_from': 'Name Example',
        'reply_to': 'emailcontactus@example.com',
        'subject': 'Subject Example',
        'message': 'Message Example'
    }
    response = client.post(reverse('api-v1:contact-list'), data=payload)
    assert response.status_code == 201
    assert response.json()


def test_contact_us_post_invalid_email():
    client = APIClient()
    payload = {
        'email_from': 'Name Example',
        'reply_to': 'emailcontactus',
        'subject': 'Subject Example',
        'message': 'Message Example'
    }
    response = client.post(reverse('api-v1:contact-list'), data=payload)
    assert response.status_code == 400
    assert response.json()['reply_to'] == ['Enter a valid email address.']


def test_contactus_patch_valid_data():
    client = APIClient()
    contact_us = ContactUs.objects.last()
    payload = {
        'subject': 'TEST SUBJ',
    }
    response = client.patch(reverse('api-v1:contact-detail', args=[contact_us.id]), data=payload)
    assert response.status_code == 200
    assert response.json()['subject'] == 'TEST SUBJ'


def test_contactus_delete():
    client = APIClient()
    contact_us = ContactUs.objects.last()
    response = client.delete(reverse('api-v1:contact-detail', args=[contact_us.id]))
    assert response.status_code == 204
    assert response.content == b''
