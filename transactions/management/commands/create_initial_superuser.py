import os
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User

class Command(BaseCommand):
    help = 'Creates or updates a superuser from environment variables'

    def handle(self, *args, **options):
        username = os.environ.get('ADMIN_USER')
        email = os.environ.get('ADMIN_EMAIL')
        password = os.environ.get('ADMIN_PASSWORD')

        if not all([username, email, password]):
            self.stdout.write(self.style.ERROR(
                'Missing ADMIN_USER, ADMIN_EMAIL, or ADMIN_PASSWORD environment variables.'
            ))
            return

        # This is the new, smarter logic
        user, created = User.objects.update_or_create(
            username=username,
            defaults={
                'email': email,
                'is_staff': True,
                'is_superuser': True,
            }
        )

        # Set the password, which ensures it's always up-to-date
        user.set_password(password)
        user.save()

        if created:
            self.stdout.write(self.style.SUCCESS(f'Superuser "{username}" was created.'))
        else:
            self.stdout.write(self.style.WARNING(f'Superuser "{username}" already existed, password has been updated.'))



    

