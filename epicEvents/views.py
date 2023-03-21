from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework import viewsets
from rest_framework import status
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from epicEvents.models import Client, Contract, Event
from epicEvents.permissions import EventPermission, ClientAndContractPermission
from epicEvents.serializers import ClientSerializer, ContractSerializer, EventSerializer, UserSerializer
from .filters import ClientFilterSet, ContractFilterSet, EventFilterSet

# Create your views here.


class ClientViewset(viewsets.ModelViewSet):
    """
    A viewset that provides CRUD operations for Client objects.

    Only authenticated users are allowed to interact with this viewset. Additionally,
    users can only interact with clients and contracts that they are associated with.
    Commercial users can only interact with clients and contracts that they are the sales
    contact for, while support users can only interact with clients that have events they
    are the support contact for. This is enforced through the `ClientAndContractPermission`
    permission class.

    This viewset supports filtering and searching by client name and email.

    """
    serializer_class = ClientSerializer
    queryset = Client.objects.all()
    permission_classes = [IsAuthenticated, ClientAndContractPermission]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_class = ClientFilterSet
    search_fields = ['full_name', 'last_name', 'email']


    def list(self, request):
        """
        Return a list of all clients that the requesting user is authorized to access.

        For commercial users, only clients they are the sales contact for will be returned.
        For support users, only clients with events they are the support contact for will
        be returned. All other users will receive a list of all clients.

        Clients can be filtered by name and email using the `search` parameter in thess
        query string. Additionally, clients can be filtered using any of the fields in
        the `ClientFilterSet`.

        Returns:
            A list of serialized clients that match the specified filters.
        """
        user = request.user
        if user.is_commercial():
            queryset = Client.objects.filter(sales_contact=user)
            queryset = self.filter_queryset(queryset)
        elif user.is_support():
            user_clients_id = Event.objects.filter(
                support_contact=user).values_list('client_id', flat=True).distinct()
            queryset = Client.objects.filter(id__in=user_clients_id)
            queryset = self.filter_queryset(queryset)
        serializer = ClientSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        """
        Create a new client object.

        The requesting user will be set as the sales contact for the client. The client
        object will be validated using the `ClientSerialier` serializer.

        Returns:
            The serialized client object on success, or a list of validation errors on failure.
        """
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.validated_data['sales_contact'] = request.user
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ContractViewset(viewsets.ModelViewSet):
    """
    A viewset for handling CRUD operations on contracts.

    Attributes:
        serializer_class: The serializer class used for serializing and deserializing contracts.
        queryset: The queryset used for retrieving contracts.
        permission_classes: The permission classes applied to the viewset.
        filter_backends: The filter backends used for filtering contracts.
        filterset_class: The filterset class used for filtering contracts.
        search_fields: The search fields used for searching contracts.
    """
    serializer_class = ContractSerializer
    queryset = Contract.objects.all()
    permission_classes = [IsAuthenticated, ClientAndContractPermission]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_class = ContractFilterSet
    search_fields = ['client_email', 'client_full_name',
                     'last_name', 'date_created', 'amount']

    def get_client(self, request):
        """
        Retrieves a client object using the provided client id in the request data.

        Args:
            request: The request object.

        Returns:
            A Client object if the client id is provided and exists, otherwise None.
        """
        client_pk = request.data.get('client')
        if client_pk:
            try:
                return Client.objects.get(pk=client_pk)
            except Client.DoesNotExist:
                return None
        return None

    def list(self, request):
        """
        Retrieves a list of contracts.

        The contracts are filtered according to the user's role:
            - commercial users can only access contracts they created.
            - support users are not allowed to access contracts.

        Args:
            request: The request object.

        Returns:
            A Response object containing the serialized contracts.
        """
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
    """
    A viewset for handling CRUD operations for Event model instances.

    list:
    Returns a list of events depending on the user's role:
        - For support users, it returns a list of all the events they are assigned to.
        - For commercial users, it returns a list of all events for their clients.

    create:
    Creates an event instance if the corresponding contract exists and is signed.

    get_client:
    Gets the client instance from the request data.

    get_contract:
    Gets the contract instance from the request data.

    check_corresponding_contract_and_client:
    Checks if the contract matches the client.

    serializer_class:
    Specifies the serializer class for the viewset.

    queryset:
    Specifies the queryset for the viewset.

    permission_classes:
    Specifies the permission classes for the viewset.

    filter_backends:
    Specifies the filter backends for the viewset.

    filterset_class:
    Specifies the filterset class for the viewset.

    search_fields:
    Specifies the search fields for the viewset.
    """

    serializer_class = EventSerializer
    queryset = Event.objects.all()
    permission_classes = [IsAuthenticated, EventPermission]
    filter_backends = [DjangoFilterBackend]
    filterset_class = EventFilterSet
    search_fields = ['client_email', 'client_full_name',
                     'last_name', 'event_date']

    def get_client(self, request):
        """
        Gets the client instance from the request data.

        Args:
            request: The HTTP request.

        Returns:
            The client instance if it exists, None otherwise.
        """
        client_pk = request.data.get('client')
        if client_pk:
            try:
                return Client.objects.get(pk=client_pk)
            except Client.DoesNotExist:
                return None
        return None

    def get_contract(self, request):
        """
        Gets the contract instance from the request data.

        Args:
            request: The HTTP request.

        Returns:
            The contract instance if it exists, None otherwise.
        """
        contract_pk = request.data.get('contract')
        if contract_pk:
            try:
                return Contract.objects.get(pk=contract_pk)
            except Contract.DoesNotExist:
                return None
        return None

    def check_corresponding_contract_and_client(self, client, contract):
        """
        Checks if the contract matches the client.

        Args:
            client: The client instance.
            contract: The contract instance.

        Returns:
            True if the contract matches the client, False otherwise.
        """
        if client.pk != contract.client.pk:
            return False
        else:
            return True

    def list(self, request):
        """
        Returns a list of events depending on the user's role:
            - For support users, it returns a list of all the events they are assigned to.
            - For commercial users, it returns a list of all events for their clients.

        Args:
            request: The HTTP request.

        Returns:
            A response with the serialized list of events.
        """
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
        """
        Overrides the default create() method to check if the given client and contract match
        and if the contract is already signed before creating the event.

        Args:
            request: the HTTP request object.
            args: positional arguments passed to the method.
            kwargs: keyword arguments passed to the method.

        Returns:
            If the given client and contract do not match, a Response object with a message indicating so.
            If the contract is not already signed, a Response object with a message indicating so.
            Otherwise, returns the result of the superclass create() method.
        """
        client = self.get_client(request)
        contract = self.get_contract(request)
        if client and contract and not self.check_corresponding_contract_and_client(client, contract):
            return Response({'event': "The contract you are indicating does not match the correct client"})
        if contract and contract.contract_status != "signed":
            return Response({'client': 'Cannot create a contract for contract that is not already signed'})
        return super().create(request, *args, **kwargs)


class UserViewset(viewsets.ModelViewSet):
    """
    A viewset that provides CRUD operations for User instances.
    Limited to Admins
    """
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]
