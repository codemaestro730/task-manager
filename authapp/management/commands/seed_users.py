from django.core.management.base import BaseCommand
from django.contrib.auth.models import User

class Command(BaseCommand):
    help = 'Seeds the database with initial user data'

    def handle(self, *args, **options):
        # Create a superuser
        try:
            if not User.objects.filter(username='admin').exists():
                User.objects.create_superuser('admin', 'admin@test.com', 'Test!2345')
                self.stdout.write(self.style.SUCCESS('Successfully created superuser'))
            else:
                self.stdout.write('Superuser already exists.')

        except Exception as e:
            self.stderr.write(f"Error: {e}")