import os
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User

class Command(BaseCommand):
    help = 'Creates a superuser from environment variables if no users exist'

    def handle(self, *args, **options):
        # Check if any users already exist in the database
        if User.objects.count() == 0:
            # Get the credentials from environment variables
            username = os.environ.get('ADMIN_USER')
            email = os.environ.get('ADMIN_EMAIL')
            password = os.environ.get('ADMIN_PASSWORD')

            if not all([username, email, password]):
                self.stdout.write(self.style.ERROR(
                    'Missing ADMIN_USER, ADMIN_EMAIL, or ADMIN_PASSWORD environment variables.'
                ))
                return

            self.stdout.write(self.style.SUCCESS(f'Creating superuser: {username}'))
            User.objects.create_superuser(username=username, email=email, password=password)
            self.stdout.write(self.style.SUCCESS('Superuser created successfully!'))
        else:
            self.stdout.write(self.style.WARNING('Users already exist, skipping superuser creation.'))
