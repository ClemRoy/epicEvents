# Generated by Django 4.1.5 on 2023-03-08 11:58

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        (
            "epicEvents",
            "0010_alter_event_attendee_number_alter_event_event_date_and_more",
        ),
    ]

    operations = [
        migrations.AlterField(
            model_name="client",
            name="client_status",
            field=models.CharField(
                choices=[("potential", "Potential Customer"), ("customer", "Customer")],
                default="potential",
                max_length=20,
            ),
        ),
        migrations.AlterField(
            model_name="contract",
            name="contract_status",
            field=models.CharField(
                choices=[
                    ("negotiation", "Contract in Negotiation"),
                    ("signed", "Contract is signed"),
                ],
                default="negotiation",
                max_length=20,
            ),
        ),
        migrations.AlterField(
            model_name="event",
            name="notes",
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
    ]