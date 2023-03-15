from rest_framework import serializers
from django.contrib.auth import get_user_model
from authentication.models import User
from epicEvents.models import Client, Contract, Event, EventStatus

User = get_user_model()


class CommercialUserValidator:
    def __call__(self, value):
        if not User.objects.filter(pk=value.pk, groups__name='commercial').exists():
            raise serializers.ValidationError(
                "The user must belong to the commercial group")


class CommercialUserField(serializers.PrimaryKeyRelatedField):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.validators.append(CommercialUserValidator())

    def to_representation(self, value):
        return value.pk


class SupportUserValidator:
    def __call__(self, value):
        if not User.objects.filter(pk=value.pk, groups__name='support').exists():
            raise serializers.ValidationError("The user must belong to the support group.")

class SupportUserField(serializers.PrimaryKeyRelatedField):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.validators.append(CommercialUserValidator())

    def to_representation(self, value):
        return value.pk



class UserSerializer(serializers.ModelSerializer):

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'email', 'password']


class ClientSerialier(serializers.ModelSerializer):
    sales_contact = CommercialUserField(queryset=User.objects.all())

    class Meta:
        model = Client
        fields = ['id', 'first_name', 'sales_contact', 'last_name', 'company_name', 'email',
                  'mobile', 'phone', 'client_status']


class ContractSerializer(serializers.ModelSerializer):
    sales_contact = CommercialUserField(queryset=User.objects.all())

    class Meta:
        model = Contract
        fields = ['id', 'client', 'sales_contact', 'contract_status',
                  'amount_due', 'payment_due_date']


class EventSerializer(serializers.ModelSerializer):
    support_contact = SupportUserField(queryset=User.objects.all())

    class Meta:
        model = Event
        fields = ['id', 'contract', 'client', 'event_status',
                  'attendee_number', 'support_contact', 'event_date']


class EventStatus(serializers.ModelSerializer):

    class Meta:
        model = EventStatus
        fields = ['id', 'status']
