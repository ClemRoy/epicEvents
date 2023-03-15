from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework import viewsets
from rest_framework import status
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from epicEvents.models import Client, Contract, Event
from epicEvents.permissions import EventPermission, ClientAndContractPermission
from epicEvents.serializers import ClientSerialier, ContractSerializer, EventSerializer, UserSerializer
from .filters import ClientFilterSet, ContractFilterSet, EventFilterSet

# Create your views here.


class ClientViewset(viewsets.ModelViewSet):
    serializer_class = ClientSerialier
    queryset = Client.objects.all()
    permission_classes = [IsAuthenticated, ClientAndContractPermission]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_class = ClientFilterSet
    search_fields = ['full_name', 'last_name', 'email']

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = self.filter_queryset(queryset)
        return queryset

    def list(self, request):
        user = request.user
        if user.is_commercial():
            queryset = Client.objects.filter(sales_contact=user)
            queryset = self.filter_queryset(queryset)
        elif user.is_support():
            user_clients_id = Event.objects.filter(
                support_contact=user).values_list('client_id', flat=True).distinct()
            queryset = Client.objects.filter(id__in=user_clients_id)
            queryset = self.filter_queryset(queryset)
        serializer = ClientSerialier(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.validated_data['sales_contact'] = request.user
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ContractViewset(viewsets.ModelViewSet):
    serializer_class = ContractSerializer
    queryset = Contract.objects.all()
    permission_classes = [IsAuthenticated, ClientAndContractPermission]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_class = ContractFilterSet
    search_fields = ['client_email', 'client_full_name',
                     'last_name', 'date_created', 'amount']

    def get_client(self, request):
        client_pk = request.data.get('client')
        if client_pk:
            try:
                return Client.objects.get(pk=client_pk)
            except Client.DoesNotExist:
                return None
        return None

    def list(self, request):
        user = request.user
        if user.is_commercial():
            queryset = Contract.objects.filter(sales_contact=request.user)
            queryset = self.filter_queryset(queryset)
            serializer = ContractSerializer(queryset, many=True)
            return Response(serializer.data)
        elif user.is_support():
            message = "Support users can't access Contratcs"
            return Response({'message': message})

    def create(self, request, *args, **kwargs):
        """
            Create a new Contract object.

            This method is called when a POST request is made to the API endpoint for creating a new Contract object.
            It first validates the request data using the serializer associated with the view. Then it checks if the
            client associated with the contract is in the 'potential' status and the new contract is 'signed'. If so,
            it updates the client status to 'customer'. It then sets the 'sales_contact' attribute of the new contract
            object to the user making the request. Finally, it creates the new contract object and returns a response
            with the data of the new contract and a status code of 201 (Created).

            Args:
                request: The HTTP request object.
                *args: Additional positional arguments.
                **kwargs: Additional keyword arguments.

            Returns:
                A response with the data of the new contract and a status code of 201 (Created), or a response with
                validation errors and a status code of 400 (Bad Request).
        """
        serializer = self.get_serializer(data=request.data)
        client = self.get_client(request)
        contract_status = request.data.get('contract_status')

        if serializer.is_valid():
            if client and client.client_status == "potential" and contract_status == 'signed':
                client.client_status = 'customer'
                client.save()
            serializer.validated_data['sales_contact'] = request.user
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EventViewset(viewsets.ModelViewSet):
    serializer_class = EventSerializer
    queryset = Event.objects.all()
    permission_classes = [IsAuthenticated, EventPermission]
    filter_backends = [DjangoFilterBackend]
    filterset_class = EventFilterSet
    search_fields = ['client_email', 'client_full_name',
                     'last_name', 'event_date']

    def get_client(self, request):
        client_pk = request.data.get('client')
        if client_pk:
            try:
                return Client.objects.get(pk=client_pk)
            except Client.DoesNotExist:
                return None
        return None

    def get_contract(self, request):
        contract_pk = request.data.get('contract')
        if contract_pk:
            try:
                return Contract.objects.get(pk=contract_pk)
            except Contract.DoesNotExist:
                return None
        return None

    def check_corresponding_contract_and_client(self, client, contract):
        if client.pk != contract.client.pk:
            return False
        else:
            return True

    def list(self, request):
        user = request.user
        if user.is_support():
            queryset = Event.objects.filter(support_contact=request.user)
            queryset = self.filter_queryset(queryset)
            serializer = EventSerializer(queryset, many=True)
            return Response(serializer.data)
        elif user.is_commercial():
            queryset = Event.objects.filter(client__sales_contact=request.user)
            queryset = self.filter_queryset(queryset)
            serializer = EventSerializer(queryset, many=True)
            return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        client = self.get_client(request)
        contract = self.get_contract(request)
        if client and contract and not self.check_corresponding_contract_and_client(client, contract):
            return Response({'event': "The contract you are indicating does not match the correct client"})
        if contract and contract.contract_status != "signed":
            return Response({'client': 'Cannot create a contract for contract that is not already signed'})
        return super().create(request, *args, **kwargs)


class UserViewset(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]
