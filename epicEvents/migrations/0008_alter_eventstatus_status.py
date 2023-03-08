# Generated by Django 4.1.5 on 2023-02-15 12:10

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("epicEvents", "0007_event_event_status"),
    ]

    operations = [
        migrations.AlterField(
            model_name="eventstatus",
            name="status",
            field=models.CharField(
                choices=[
                    ("preparation", "In Preparation"),
                    ("ongoig", "On going"),
                    ("finished", "Finished"),
                ],
                max_length=20,
            ),
        ),
    ]
