from rest_framework import serializers
from authentication.models import User
from epicEvents.models import Client, Contract, Event,EventStatus


class UserSerializer(serializers.ModelSerializer):

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'email', 'password']


class ClientSerialier(serializers.ModelSerializer):

    class Meta:
        model = Client
        fields = ['id', 'first_name', 'last_name', 'company_name', 'email',
                  'mobile', 'phone', 'client_status']


class ContractSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contract
        fields = ['id', 'client', 'contract_status',
                  'amount_due', 'payment_due_date']


class EventSerializer(serializers.ModelSerializer):

    class Meta:
        model = Event
        fields = ['id', 'contract', 'client', 'event_status',
                  'attendee_number', 'event_date']

class EventStatus(serializers.ModelSerializer):

    class Meta:
        model = EventStatus
        fields = ['id', 'status']