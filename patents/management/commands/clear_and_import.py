from django.core.management.base import BaseCommand
from django.core.management import call_command
from patents.models import Copyright, PatentFiled, PatentGranted


class Command(BaseCommand):
    help = 'Clear all existing data and re-import from CSV files'

    def add_arguments(self, parser):
        parser.add_argument(
            '--diagnostic',
            action='store_true',
            help='Pass cleanup diagnostics through to import_csv',
        )
        parser.add_argument(
            '--diagnostic-limit',
            type=int,
            default=10,
            help='Maximum sample row entries shown per exclusion reason (default: 10)',
        )
        parser.add_argument(
            '--strict-exclusions',
            action='store_true',
            help='Fail if any rows are excluded during cleanup import',
        )

    def handle(self, *args, **options):
        # Clear existing data
        self.stdout.write(self.style.WARNING('Clearing existing data...'))
        
        copyright_count = Copyright.objects.count()
        filed_count = PatentFiled.objects.count()
        granted_count = PatentGranted.objects.count()
        
        Copyright.objects.all().delete()
        PatentFiled.objects.all().delete()
        PatentGranted.objects.all().delete()
        
        self.stdout.write(self.style.SUCCESS(f'Deleted {copyright_count} copyrights'))
        self.stdout.write(self.style.SUCCESS(f'Deleted {filed_count} filed patents'))
        self.stdout.write(self.style.SUCCESS(f'Deleted {granted_count} granted patents'))
        
        # Import fresh data
        self.stdout.write(self.style.WARNING('\nImporting fresh data from CSV files...'))
        call_command(
            'import_csv',
            diagnostic=options.get('diagnostic', False),
            diagnostic_limit=max(1, options.get('diagnostic_limit', 10) or 10),
            strict_exclusions=options.get('strict_exclusions', False),
        )
        
        self.stdout.write(self.style.SUCCESS('\nFresh import completed!'))
