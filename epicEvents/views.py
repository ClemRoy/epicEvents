from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import viewsets
from epicEvents.models import Client, Contract, Event
from epicEvents.serializers import ClientSerialier, ContractSerializer, EventSerializer

# Create your views here.


class ClientViewset(viewsets.ModelViewSet):
    serializer_class = ClientSerialier
    queryset = Client.objects.all()

    def list(self, request):
        queryset = Client.objects.all()
        serializer = ClientSerialier(queryset, many=True)
        return Response(serializer.data)

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class ContractViewset(viewsets.ModelViewSet):
    serializer_class = ContractSerializer
    queryset = Contract.objects.all()


class EventViewset(viewsets.ModelViewSet):
    serializer_class = EventSerializer
    queryset = Event.objects.all()
