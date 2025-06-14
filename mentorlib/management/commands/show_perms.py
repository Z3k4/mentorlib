from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import Permission


class Command(BaseCommand):
    help = "Show all available permissions"

    def add_arguments(self, parser):
        parser.add_argument("-m", nargs="+", type=str, default=None)

    def handle(self, *args, **options):
        queryset = Permission.objects.all()
        
        for perm in queryset:
            if perm.content_type.model in options['m']:
                self.stdout.write(f"{perm.content_type.model}.{perm.codename}")