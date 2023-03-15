from django_filters import rest_framework as filters
from django.db.models import Q
from epicEvents.models import Client, Contract, Event


class ClientFilterSet(filters.FilterSet):
    """
    A filterset for filtering Client records by their name and email fields.

    Filters:
    - full_name: Filter by client's first or last name, case-insensitive.
    - last_name: Filter by client's last name, case-insensitive.
    - email: Filter by client's email address, case-insensitive.

    Methods:
    - filter_full_name: Custom filter method to filter by client's full name.
    """

    full_name = filters.CharFilter(method='filter_by_fullname')
    last_name = filters.CharFilter(
        field_name="last_name", lookup_expr='name__iexact')
    email = filters.CharFilter(field_name='email', lookup_expr='iexact')

    def filter_full_name(self, queryset, name, value):
        queryset = queryset.filter(
            Q(first_name__iexact=value) |
            Q(last_name__iexact=value)
        )
        return queryset

    class Meta:
        model = Client
        fields = ['full_name', 'last_name', 'email']


class ContractFilterSet(filters.FilterSet):
    """
    A `FilterSet` for filtering `Contract` instances.

    The following filters are available:
    - `client_email`: filters by the exact email of the associated client.
    - `client_full_name`: filters by the exact first or last name of the associated client.
    - `last_name`: filters by the exact last name of the associated client.
    - `date_created`: filters by the exact creation date of the contract.
    - `amount`: filters by the exact amount due of the contract.

    Note: the `client_full_name` and `last_name` filters are case-insensitive.

    Examples:
    To filter contracts by the email 'john@example.com', use:
        /api/contracts?client_email=john@example.com

    To filter contracts by the last name 'Doe', use:
        /api/contracts?last_name=Doe

    To filter contracts by the full name 'John Doe', use:
        /api/contracts?client_full_name=John Doe
    """
    client_email = filters.CharFilter(
        field_name='client__email', lookup_expr='iexact')
    client_full_name = filters.CharFilter(method='filter_client_full_name')
    last_name = filters.CharFilter(
        field_name='client__last_name', lookup_expr='iexact')
    date_created = filters.DateFilter(
        field_name='date_created', lookup_expr='iexact')
    amount = filters.NumberFilter(field_name='amount_due')

    def filter_client_full_name(self, queryset, name, value):
        queryset = queryset.filter(
            Q(client__first_name__iexact=value) |
            Q(client__last_name__iexact=value)
        )
        return queryset

    class Meta:
        model = Contract
        fields = ['client_email', 'client_full_name',
                  'last_name', 'date_created', 'amount']


class EventFilterSet(filters.FilterSet):
    """A FilterSet class for filtering Event instances by client email, client full name, last name, and event date.

    The filter fields available in this class are:

    - client_email: filters events based on the email of their associated client, using the "icontains" lookup expression.
    - client_full_name: filters events based on the full name of their associated client, using a custom filter method.
    - last_name: filters events based on the last name of their associated client, using the "iexact" lookup expression.
    - event_date: filters events based on their event date, using the "exact" lookup expression.

    The custom filter method "filter_client_full_name" searches for clients whose first name or last name match the provided value, using the "iexact" lookup expression.

    """
    client_email = filters.CharFilter(
        field_name='client__email', lookup_expr='icontains')
    client_full_name = filters.CharFilter(method='filter_client_full_name')
    last_name = filters.CharFilter(
        field_name='client__last_name', lookup_expr='iexact')
    event_date = filters.DateFilter(
        field_name='event_date', lookup_expr='exact')

    def filter_client_full_name(self, queryset, name, value):
        queryset = queryset.filter(
            Q(client__first_name__iexact=value) |
            Q(client__last_name__iexact=value)
        )
        return queryset

    class Meta:
        model = Event
        fields = ['client_email', 'client_full_name',
                  'last_name', 'event_date']
