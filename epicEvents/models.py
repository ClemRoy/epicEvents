from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.


class Client(models.Model):
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
        settings.AUTH_USER_MODEL, blank=True, null=True, on_delete=models.SET_NULL)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "Client: " + self.company_name


class Contract(models.Model):
    CONTRACT_STATUS_CHOICES = [
        ('negotiation', 'Contract in Negotiation'),
        ('signed', 'Contract is signed'),
    ]
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    sales_contact = models.ForeignKey(
        settings.AUTH_USER_MODEL, null=True, on_delete=models.SET_NULL)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    contract_status = models.CharField(
        max_length=20, default='negotiation', choices=CONTRACT_STATUS_CHOICES)
    amount_due = models.FloatField()
    payment_due_date = models.DateField()

    def __str__(self):
        return "Contrat:" + str(self.client) + " " + str(self.date_created)


class EventStatus(models.Model):
    EVENT_STATUS_CHOICES = [
        ('preparation', 'In Preparation'),
        ('ongoig', 'On going'),
        ('finished', 'Finished')
    ]
    status = models.CharField(max_length=20, choices=EVENT_STATUS_CHOICES)

    def __str__(self):
        return "Event Status:" + self.status


class Event(models.Model):
    contract = models.ForeignKey(Contract, on_delete=models.CASCADE)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    support_contact = models.ForeignKey(
        settings.AUTH_USER_MODEL, blank=True, null=True, on_delete=models.SET_NULL)
    event_status = models.ForeignKey(
        EventStatus, null=True, default='1', on_delete=models.SET_NULL)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    attendee_number = models.IntegerField()
    event_date = models.DateField()
    notes = models.CharField(max_length=500)

    def __str__(self):
        return "Event: " + str(self.contract)
