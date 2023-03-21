from django.core.management.base import BaseCommand
from utils.faker import generate_fake_data
class Command(BaseCommand):
    help = 'Prints a message to the console'

    def handle(self, *args, **options):
        generate_fake_data()
        self.stdout.write(self.style.SUCCESS('create fake data'))