from rest_framework import serializers
from django.contrib.auth import get_user_model
from authentication.models import User
from epicEvents.models import Client, Contract, Event, EventStatus

User = get_user_model()


class CommercialUserValidator:
    """
    Validator to ensure that a user belongs to the commercial group.

    Raises a `serializers.ValidationError` if the given value does not belong to the
    commercial group.

    Usage:
    ```
    class MySerializer(serializers.ModelSerializer):
        sales_contact = serializers.PrimaryKeyRelatedField(
            queryset=User.objects.all(),
            validators=[CommercialUserValidator()]
        )
        ...
    ```
    """
    def __call__(self, value):
        """
        A validator that checks if a user belongs to the commercial group.
        It raises a serializers.ValidationError if the user does not belong to the commercial group.

        Args:
            value: A User object.

        Raises:
            serializers.ValidationError: If the user does not belong to the commercial group.

        """
        if not User.objects.filter(pk=value.pk, groups__name='commercial').exists():
            raise serializers.ValidationError(
                "The user must belong to the commercial group")


class CommercialUserField(serializers.PrimaryKeyRelatedField):
    """
    A custom PrimaryKeyRelatedField that only accepts users belonging to the commercial group.
    """
    
    def __init__(self, **kwargs):
        """
        Initializes a new instance of the CommercialUserField.
        
        Parameters:
        -----------
        kwargs : dict
            Additional keyword arguments to be passed to the base class constructor.
        """
        super().__init__(**kwargs)
        self.validators.append(CommercialUserValidator())

    def to_representation(self, value):
        """
        Converts the input value into a representation suitable for serialization.
        
        Parameters:
        -----------
        value : object
            The object to be represented.
            
        Returns:
        --------
        object
            The representation of the input object.
        """
        return value.pk


class SupportUserValidator:
    """
    Validator to ensure that a user belongs to the 'support' group.
    """
    def __call__(self, value):
        """
        Checks if the user associated with the given value belongs to the 'support' group. If not, raises a 
        serializers.ValidationError.

        Parameters:
        -----------
        value : django.contrib.auth.models.User
            User instance to be validated.

        Returns:
        --------
        None
        """
        if not User.objects.filter(pk=value.pk, groups__name='support').exists():
            raise serializers.ValidationError("The user must belong to the support group.")

class SupportUserField(serializers.PrimaryKeyRelatedField):
    """
    A custom primary key related field that only allows users belonging to the "support" group.

    Inherits from `serializers.PrimaryKeyRelatedField`.

    Raises a `serializers.ValidationError` if the user does not belong to the "support" group.

    Attributes:
    -----------
    All attributes of `serializers.PrimaryKeyRelatedField`.

    Methods:
    --------
    to_representation:
        Returns the primary key of the related object.
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.validators.append(SupportUserValidator())

    def to_representation(self, value):
        """
        Returns the primary key of the related object.

        Parameters:
        -----------
        value: Any
            The related object.

        Returns:
        --------
        Any
            The primary key of the related object.
        """
        return value.pk


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for creating a new User instance.

    The create() method creates a new User instance with the validated data.

    Args:
        serializers.ModelSerializer: Inherits from ModelSerializer, which
        provides a set of default behavior for model instances.

    Returns:
        User: The newly created User instance.

    Raises:
        N/A
    """
    def create(self, validated_data):
        """
        Create a new User instance with the validated data.

        Args:
            validated_data (dict): Validated data for the new User instance.

        Returns:
            User: The newly created User instance.

        Raises:
            N/A
        """
        user = User.objects.create_user(**validated_data)
        return user

    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'email', 'password']


class ClientSerializer(serializers.ModelSerializer):
    """
    Serializer class for Client model.

    Serializes and deserializes Client instances to and from JSON format.

    Fields:
    - id: int - read-only field representing the ID of the client.
    - first_name: str - required field representing the first name of the client.
    - sales_contact: CommercialUserField - field representing the sales contact for the client.
    - last_name: str - required field representing the last name of the client.
    - company_name: str - optional field representing the name of the company of the client.
    - email: str - required field representing the email address of the client.
    - mobile: str - optional field representing the mobile number of the client.
    - phone: str - optional field representing the phone number of the client.
    - client_status: ClientStatus - required field representing the status of the client.

    Methods:
    - create(self, validated_data): creates a new Client instance using validated data.
    """
    sales_contact = CommercialUserField(queryset=User.objects.all())

    class Meta:
        model = Client
        fields = ['id', 'first_name', 'sales_contact', 'last_name', 'company_name', 'email',
                  'mobile', 'phone', 'client_status']


class ContractSerializer(serializers.ModelSerializer):
    """
    Serializer for the Contract model. Includes the following fields:
    - id (int): The ID of the Contract object.
    - client (int): The ID of the related Client object.
    - sales_contact (int): The ID of the User object that is associated with the contract.
    - contract_status (str): The current status of the contract.
    - amount_due (float): The amount of money due for the contract.
    - payment_due_date (date): The due date for payment of the contract.

    The sales_contact field is represented as a CommercialUserField, which is a PrimaryKeyRelatedField that is restricted to User objects that belong to the 'commercial' group.

    This serializer has no custom methods.
    """
    sales_contact = CommercialUserField(queryset=User.objects.all())

    class Meta:
        model = Contract
        fields = ['id', 'client', 'sales_contact','date_created', 'contract_status',
                  'amount_due', 'payment_due_date']


class EventSerializer(serializers.ModelSerializer):
    """
    Serializer for the Event model. The support_contact field is a PrimaryKeyRelatedField that is 
    validated to only accept users that belong to the 'support' group using the SupportUserField 
    validator. 
    """
    support_contact = SupportUserField(queryset=User.objects.all())

    class Meta:
        model = Event
        fields = ['id', 'contract', 'client', 'event_status',
                  'attendee_number', 'support_contact', 'event_date']


class EventStatus(serializers.ModelSerializer):
    """
    Serializer for the EventStatus model.

    Fields:
    - id: Integer field for the event status ID.
    - status: String field for the event status.
    """
    class Meta:
        model = EventStatus
        fields = ['id', 'status']
