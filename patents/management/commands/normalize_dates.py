from django.core.management.base import BaseCommand
from patents.models import Copyright, PatentFiled, PatentGranted
from patents.utils.csv_preprocessing import normalize_date_text, normalize_publication_status, normalize_year


class Command(BaseCommand):
    help = 'Normalize date formats in the database (convert dd.mm.yyyy to dd/mm/yyyy)'

    def normalize_date(self, date_str):
        """Convert date formats to dd/mm/yyyy"""
        return normalize_date_text(date_str)

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Starting date normalization...'))
        
        # Normalize Copyright dates
        copyrights_updated = 0
        for copyright in Copyright.objects.all():
            updated = False
            
            if copyright.year:
                normalized = normalize_year(copyright.year)
                if normalized != copyright.year:
                    copyright.year = normalized
                    updated = True
            
            if updated:
                copyright.save()
                copyrights_updated += 1
        
        self.stdout.write(self.style.SUCCESS(f'Updated {copyrights_updated} copyright records'))
        
        # Normalize PatentFiled dates
        filed_updated = 0
        for patent in PatentFiled.objects.all():
            updated = False
            
            if patent.date_of_filing:
                normalized = self.normalize_date(patent.date_of_filing)
                if normalized != patent.date_of_filing:
                    patent.date_of_filing = normalized
                    updated = True
            
            if patent.date_of_publication:
                normalized = normalize_publication_status(patent.date_of_publication)
                if normalized != patent.date_of_publication:
                    patent.date_of_publication = normalized
                    updated = True
            
            if updated:
                patent.save()
                filed_updated += 1
        
        self.stdout.write(self.style.SUCCESS(f'Updated {filed_updated} filed patent records'))
        
        # Normalize PatentGranted dates
        granted_updated = 0
        for patent in PatentGranted.objects.all():
            updated = False
            
            if patent.date_of_grant:
                normalized = self.normalize_date(patent.date_of_grant)
                if normalized != patent.date_of_grant:
                    patent.date_of_grant = normalized
                    updated = True
            
            if patent.date_of_publication:
                normalized = normalize_publication_status(patent.date_of_publication)
                if normalized != patent.date_of_publication:
                    patent.date_of_publication = normalized
                    updated = True
            
            if updated:
                patent.save()
                granted_updated += 1
        
        self.stdout.write(self.style.SUCCESS(f'Updated {granted_updated} granted patent records'))
        
        self.stdout.write(self.style.SUCCESS('Date normalization completed!'))
        self.stdout.write(self.style.SUCCESS(f'Total records updated: {copyrights_updated + filed_updated + granted_updated}'))
