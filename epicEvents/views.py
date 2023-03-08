from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets
from rest_framework import status
from epicEvents.models import Client, Contract, Event
from epicEvents.permissions import EventPermission,ClientAndContractPermission
from epicEvents.serializers import ClientSerialier, ContractSerializer, EventSerializer, UserSerializer

# Create your views here.


class ClientViewset(viewsets.ModelViewSet):
    serializer_class = ClientSerialier
    queryset = Client.objects.all()
    permission_classes = [ IsAuthenticated,ClientAndContractPermission]


    def list(self, request):
        queryset = Client.objects.all()
        serializer = ClientSerialier(queryset, many=True)
        return Response(serializer.data)

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ContractViewset(viewsets.ModelViewSet):
    serializer_class = ContractSerializer
    queryset = Contract.objects.all()
    permission_classes = [IsAuthenticated,ClientAndContractPermission]

    def get_client(self,request):
        client_pk = request.data.get('client')
        if client_pk:
            try:
                return Client.objects.get(pk=client_pk)
            except Client.DoesNotExist:
                return None
        return None

    def list(self, request):
        queryset = Contract.objects.all()
        serializer = ContractSerializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        client = self.get_client(request)
        print(request.data)
        contract_status = request.data.get('contract_status')
        if client and client.client_status == "potential" and contract_status == 'signed':
            client.client_status = 'customer'
            client.save()
        return super().create(request, *args, **kwargs)


class EventViewset(viewsets.ModelViewSet):
    serializer_class = EventSerializer
    queryset = Event.objects.all()
    permission_classes = [IsAuthenticated,EventPermission]

    def get_client(self,request):
        client_pk = request.data.get('client')
        if client_pk:
            try:
                return Client.objects.get(pk=client_pk)
            except Client.DoesNotExist:
                return None
        return None

    def get_contract(self,request):
        contract_pk = request.data.get('contract')
        if contract_pk:
            try:
                return Contract.objects.get(pk=contract_pk)
            except Contract.DoesNotExist:
                return None
        return None

    def check_corresponding_contract_and_client(self,client,contract):
        if client.pk != contract.client.pk:
            return False
        else:
            return True


    def list(self, request):
        queryset = Event.objects.all()
        serializer = EventSerializer(queryset, many=True)
        return Response(serializer.data)
    
    def create(self, request, *args, **kwargs):
        client = self.get_client(request)
        contract = self.get_contract(request)
        if client and contract and not self.check_corresponding_contract_and_client(client,contract):
            return Response({'event':"The contract you are indicating does not match the correct client"})
        if contract and contract.contract_status != "signed":
            return Response({'client':'Cannot create a contract for contract that is not already signed'})
        return super().create(request, *args, **kwargs)

class UserViewset(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
