from api.tasks import send_email

from currency.models import ContactUs, Rate, Source

from rest_framework import serializers


class RateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rate
        fields = (
            'id',
            'sale',
            'buy',
            'source',
            'type',
            'base_type',
            'created',
        )


class SourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Source
        fields = (
            'id',
            'name',
            'source_url',
        )


class ContactUsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactUs
        fields = (
            'id',
            'email_from',
            'reply_to',
            'subject',
            'message',
            'created',
        )

    def create(self, validated_data):
        send_email.delay(**validated_data)
        return ContactUs.objects.create(**validated_data)
