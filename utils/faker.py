from epicEvents.models import Client,Contract,Event,EventStatus
from authentication.models import User
from django.contrib.auth.models import Group
from django.utils import timezone
from django.shortcuts import get_object_or_404
import random
from random import randint
from datetime import date, timedelta
from faker import Faker



def generate_fake_data():
    """
    It creates a client, creates a contract for that client, and creates an event for that contract.
    """
    fake = Faker()
    sales_contact = User.objects.filter(groups__name='commercial').first()
    support_contact = User.objects.filter(groups__name='support').first()

    start_date = timezone.now().date()
    end_date = start_date + timedelta(days=364)
    future_date = fake.date_between(start_date=start_date, end_date=end_date)
    for i in range(25):
        client = Client.objects.create(
            first_name=fake.first_name()[:random.randint(5, 25)],
            last_name=fake.last_name()[:random.randint(5, 25)],
            company_name = fake.company()[:random.randint(5, 255)],
            email=fake.email()[:random.randint(5, 60)],
            mobile=fake.phone_number()[:random.randint(5, 20)],
            phone=fake.phone_number()[:random.randint(5, 20)],
            client_status=random.choice([c[0] for c in Client.CLIENT_STATUS_CHOICES]),
            sales_contact=sales_contact,
            date_created=timezone.now(),
            date_updated=timezone.now(),
        )
        client.save()
        for j in range(50):
            start_date = timezone.now().date()
            end_date = start_date + timedelta(days=364)
            future_date = fake.date_between(start_date=start_date, end_date=end_date)
            random_float = fake.pyfloat(left_digits=5, right_digits=2)
            contract = Contract(
                client = client,
                sales_contact = sales_contact,
                contract_status = random.choice([c[0] for c in Contract.CONTRACT_STATUS_CHOICES]),
                date_created = timezone.now(),
                date_updated = timezone.now(),
                amount_due = random_float,
                payment_due_date = future_date,
            )
            contract.save()
            for k in range(2):
                start_date = timezone.now().date()
                event_date = fake.date_time_between(start_date='now', end_date='+30d', tzinfo=timezone.utc)
                event = Event.objects.create(
                    contract = contract,
                    event_date = event_date,
                    client = client,
                    support_contact = support_contact,
                    event_status = get_object_or_404(EventStatus, pk= randint(1,3)),
                    attendee_number = fake.pyint(min_value=0, max_value=100),
                    date_created = timezone.now(),
                    date_updated = timezone.now(),
                    notes = fake.text(max_nb_chars=500),
                )
                event.save()

