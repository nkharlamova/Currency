from currency.models import ContactUs

from django.conf import settings


def test_index(client):
    response = client.get('/')
    assert response.status_code == 200


def test_contact_us_get(client):
    response = client.get('/currency/contact-us/create/')
    assert response.status_code == 200


def test_contact_us_post_empty_data(client):
    response = client.post('/currency/contact-us/create/')
    assert response.status_code == 200  # when post 200 is error
    assert response.context_data['form'].errors == {
        'email_from': ['This field is required.'],
        'reply_to': ['This field is required.'],
        'subject': ['This field is required.'],
        'message': ['This field is required.']
    }


def test_contact_us_post_valid_data(client, mailoutbox):
    initial_count = ContactUs.objects.count()

    payload = {
        'email_from': 'Name Example',
        'reply_to': 'emailcontactus@example.com',
        'subject': 'Subject Example',
        'message': 'Example Text\n' * 10
    }
    response = client.post('/currency/contact-us/create/', data=payload)
    assert response.status_code == 302
    assert response.url == '/currency/contacts/list/'

    assert len(mailoutbox) == 1
    assert mailoutbox[0].to == [settings.EMAIL_HOST_USER]
    assert mailoutbox[0].subject == 'User ContactUs'

    assert ContactUs.objects.count() == initial_count + 1


def test_contact_us_post_invalid_email(client, mailoutbox):
    initial_count = ContactUs.objects.count()

    payload = {
        'email_from': 'Name Example',
        'reply_to': 'emailcontactus',
        'subject': 'Subject Example',
        'message': 'Example Text\n' * 10
    }
    response = client.post('/currency/contact-us/create/', data=payload)
    assert response.status_code == 200
    assert response.context_data['form'].errors == {'reply_to': ['Enter a valid email address.']}
    assert len(mailoutbox) == 0

    assert ContactUs.objects.count() == initial_count
