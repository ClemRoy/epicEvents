from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.


class Client(models.Model):
    """
    Model to represent a client, including contact information and their status.
    """
    CLIENT_STATUS_CHOICES = [
        ('potential', 'Potential Customer'),
        ('customer', 'Customer')
    ]
    first_name = models.CharField(max_length=25)
    last_name = models.CharField(max_length=25)
    company_name = models.CharField(max_length=255)
    email = models.EmailField(max_length=60, unique=True)
    mobile = models.CharField(max_length=20)
    phone = models.CharField(max_length=20)
    client_status = models.CharField(
        max_length=20, default='potential', choices=CLIENT_STATUS_CHOICES)
    sales_contact = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, limit_choices_to={'groups__name': 'commercial'})
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def full_name(self):
        """
        Returns the full name of the client by concatenating the first and last name.
        """
        return f"{self.first_name} {self.last_name}"

    def __str__(self):
        """
        Returns a string representation of the Client instance, which is used in the Django admin and other places
        where the object needs to be displayed as a string.
        
        The string representation includes the client's ID and company name.
        """
        return f"Id: {self.pk}, Client: {self.company_name}"


class Contract(models.Model):

    """
    A model representing a contract.

    Fields:
    - client: the client associated with the contract (ForeignKey to Client model)
    - sales_contact: the sales contact associated with the contract (ForeignKey to User model)
    - date_created: the date the contract was created (auto-generated DateTimeField)
    - date_updated: the date the contract was last updated (auto-generated DateTimeField)
    - contract_status: the status of the contract (choices defined in CONTRACT_STATUS_CHOICES)
    - amount_due: the amount due for the contract (FloatField)
    - payment_due_date: the due date for the contract payment (DateField)
    """

    CONTRACT_STATUS_CHOICES = [
        ('negotiation', 'Contract in Negotiation'),
        ('signed', 'Contract is signed'),
    ]
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    sales_contact = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, limit_choices_to={'groups__name': 'commercial'})
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    contract_status = models.CharField(
        max_length=20, default='negotiation', choices=CONTRACT_STATUS_CHOICES)
    amount_due = models.FloatField()
    payment_due_date = models.DateField()

    def __str__(self):
        """
        Returns a string representation of the contract, including its ID, associated client,
        creation date, and status.
        """        
        return f"Id: {self.pk}, Contrat: {str(self.client )}, date: {str(self.date_created)}, status: {str(self.contract_status)}"


# The EventStatus object is meant to be hardcoded DO NOT CREATE NEW INSTANCES

class EventStatus(models.Model):
    """
    A model representing the status of an event.

    Note:
        /!\This object instance should never be modified by the users.

    Attributes:
        EVENT_STATUS_CHOICES (tuple): The available choices for the event status.
        status (str): The status of the event.

    Methods:
        __str__(): Returns the string representation of the event status object.
    """
    EVENT_STATUS_CHOICES = [
        ('preparation', 'In Preparation'),
        ('ongoig', 'On going'),
        ('finished', 'Finished')
    ]
    status = models.CharField(max_length=20, choices=EVENT_STATUS_CHOICES)

    def __str__(self):
        """
        Returns the string representation of the event status object.

        Returns:
            str: A string representing the status of the event.
        """
        return f"Event Status: {self.status}"


class Event(models.Model):
    """
    A model representing an event associated with a contract and a client.

    Users should not modify instances of this class directly, as they are created and
    managed by the application.

    Attributes:
        contract (ForeignKey): A foreign key to the contract associated with the event.
        client (ForeignKey): A foreign key to the client associated with the event.
        support_contact (ForeignKey): A foreign key to the support user associated with the event.
        event_status (ForeignKey): A foreign key to the status of the event.
        date_created (DateTimeField): The date and time the event was created.
        date_updated (DateTimeField): The date and time the event was last updated.
        attendee_number (IntegerField): The number of attendees expected at the event.
        event_date (DateField): The date of the event.
        notes (CharField): Additional notes about the event.

    Methods:
        __str__(): Returns a string representation of the event object.
    """
    contract = models.ForeignKey(Contract, on_delete=models.CASCADE)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    support_contact = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, limit_choices_to={'groups__name': 'support'})
    event_status = models.ForeignKey(
        EventStatus, default='1', on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    attendee_number = models.IntegerField()
    event_date = models.DateField()
    notes = models.CharField(max_length=500, blank=True, null=True)

    def __str__(self):
        """
        Returns a string representation of the event object.

        Returns:
            str: A string representing the event object, including the associated contract,
            the event date, and the current event status.
        """
        return f"Event: {str(self.contract.client)}, Event date: {self.event_date}, {self.event_status}"
