from django.db import models
from django.conf import settings
# Create your models here.

from django.contrib.auth.models import AbstractUser
from django.db import models


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
        max_length=20, choices=CLIENT_STATUS_CHOICES)
    sales_contact = models.ForeignKey(
        settings.AUTH_USER_MODEL, blank=True, null=True, on_delete=models.SET_NULL)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)


class Contract(models.Model):
    CONTRACT_STATUS_CHOICES = [
        ('negotiation', 'Contract in Negotiation'),
        ('signed', 'Contract is signed'),
    ]
    client = models.ForeignKey(Client, blank=True, on_delete=models.CASCADE)
    sales_contact = models.ForeignKey(
        settings.AUTH_USER_MODEL, blank=True,null=True, on_delete=models.SET_NULL)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    contract_status = models.CharField(
        max_length=20, choices=CONTRACT_STATUS_CHOICES)
    amount_due = models.FloatField(blank=True)
    payment_due_date = models.DateField(blank=True)


class Event(models.Model):
    EVENT_STATUS_CHOICES = [
        ('preparation', 'In Preparation'),
        ('ongoing', 'Ongoing'),
        ('finished', 'Finished')
    ]
    contract = models.ForeignKey(Contract, on_delete=models.CASCADE)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    support_contact = models.ForeignKey(
        settings.AUTH_USER_MODEL, blank=True,null=True, on_delete=models.SET_NULL)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    event_status = models.CharField(
        max_length=20, choices=EVENT_STATUS_CHOICES)
    attendee_number = models.IntegerField(blank=True)
    event_date = models.DateField(blank=True)
    notes = models.CharField(max_length=500, blank=True)
