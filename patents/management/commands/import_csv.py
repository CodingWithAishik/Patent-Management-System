import csv
import os
from django.core.management.base import BaseCommand
from django.conf import settings
from patents.models import Copyright, PatentFiled, PatentGranted


class Command(BaseCommand):
    help = 'Import data from CSV files into the database'

    def handle(self, *args, **options):
        base_dir = settings.BASE_DIR
        
        # Import Copyrights
        self.stdout.write(self.style.WARNING('Importing Copyrights...'))
        copyright_file = base_dir / 'Copy of Patent_Details_filtered.xlsx - Copy rights.csv'
        self.import_copyrights(copyright_file)
        
        # Import Filed Patents
        self.stdout.write(self.style.WARNING('\nImporting Filed Patents...'))
        filed_file = base_dir / 'Copy of Patent_Details_filtered.xlsx - Patents (Filed).csv'
        self.import_filed_patents(filed_file)
        
        # Import Granted Patents
        self.stdout.write(self.style.WARNING('\nImporting Granted Patents...'))
        granted_file = base_dir / 'Copy of Patent_Details_filtered.xlsx - Patents (Granted).csv'
        self.import_granted_patents(granted_file)
        
        self.stdout.write(self.style.SUCCESS('\n\nImport completed successfully!'))
        self.stdout.write(f'Copyrights: {Copyright.objects.count()}')
        self.stdout.write(f'Patents Filed: {PatentFiled.objects.count()}')
        self.stdout.write(f'Patents Granted: {PatentGranted.objects.count()}')

    def import_copyrights(self, file_path):
        """Import copyright data from CSV"""
        if not os.path.exists(file_path):
            self.stdout.write(self.style.ERROR(f'File not found: {file_path}'))
            return
        
        with open(file_path, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            rows = list(reader)
            
            # Find the header row (contains "Sl. No.")
            header_row_idx = None
            for idx, row in enumerate(rows):
                if row and 'Sl. No.' in str(row[0]):
                    header_row_idx = idx
                    break
            
            if header_row_idx is None:
                self.stdout.write(self.style.ERROR('Could not find header row'))
                return
            
            # Start importing from the next row after header
            count = 0
            for row in rows[header_row_idx + 1:]:
                # Skip empty rows
                if not any(row):
                    continue
                
                # Skip rows that don't have proper data
                if len(row) < 4:
                    continue
                
                try:
                    Copyright.objects.create(
                        sl_no=self.safe_int(row[0]) if len(row) > 0 else None,
                        year=row[1].strip() if len(row) > 1 and row[1] else None,
                        faculty_students=row[2].strip() if len(row) > 2 and row[2] else None,
                        title=row[3].strip() if len(row) > 3 and row[3] else None,
                        filing_info=row[4].strip() if len(row) > 4 and row[4] else None,
                        inventors=row[5].strip() if len(row) > 5 and row[5] else None,
                    )
                    count += 1
                except Exception as e:
                    self.stdout.write(self.style.WARNING(f'Skipped row: {e}'))
            
            self.stdout.write(self.style.SUCCESS(f'Imported {count} copyright records'))

    def import_filed_patents(self, file_path):
        """Import filed patent data from CSV"""
        if not os.path.exists(file_path):
            self.stdout.write(self.style.ERROR(f'File not found: {file_path}'))
            return
        
        with open(file_path, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            rows = list(reader)
            
            # Find the header row
            header_row_idx = None
            for idx, row in enumerate(rows):
                if row and 'Sl. No.' in str(row[0]):
                    header_row_idx = idx
                    break
            
            if header_row_idx is None:
                self.stdout.write(self.style.ERROR('Could not find header row'))
                return
            
            count = 0
            for row in rows[header_row_idx + 1:]:
                # Skip empty rows or year headers
                if not any(row) or (len(row) == 1 and row[0].strip().isdigit() and len(row[0].strip()) == 4):
                    continue
                
                # Skip rows that don't have sufficient data
                if len(row) < 4:
                    continue
                
                try:
                    PatentFiled.objects.create(
                        sl_no=self.safe_int(row[0]) if len(row) > 0 else None,
                        date_of_filing=row[1].strip() if len(row) > 1 and row[1] else None,
                        inventors=row[2].strip() if len(row) > 2 and row[2] else None,
                        title=row[3].strip() if len(row) > 3 and row[3] else None,
                        application_number=row[4].strip() if len(row) > 4 and row[4] else None,
                        date_of_publication=row[5].strip() if len(row) > 5 and row[5] else None,
                        abstract=row[6].strip() if len(row) > 6 and row[6] else None,
                        applicant_name=row[7].strip() if len(row) > 7 and row[7] else None,
                    )
                    count += 1
                except Exception as e:
                    self.stdout.write(self.style.WARNING(f'Skipped row: {e}'))
            
            self.stdout.write(self.style.SUCCESS(f'Imported {count} filed patent records'))

    def import_granted_patents(self, file_path):
        """Import granted patent data from CSV"""
        if not os.path.exists(file_path):
            self.stdout.write(self.style.ERROR(f'File not found: {file_path}'))
            return
        
        with open(file_path, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            rows = list(reader)
            
            # Find the header row
            header_row_idx = None
            for idx, row in enumerate(rows):
                if row and 'Sl. No.' in str(row[0]):
                    header_row_idx = idx
                    break
            
            if header_row_idx is None:
                self.stdout.write(self.style.ERROR('Could not find header row'))
                return
            
            count = 0
            for row in rows[header_row_idx + 1:]:
                # Skip empty rows or year headers
                if not any(row) or (len(row) == 1 and row[0].strip().isdigit() and len(row[0].strip()) == 4):
                    continue
                
                # Skip rows that don't have sufficient data
                if len(row) < 5:
                    continue
                
                try:
                    PatentGranted.objects.create(
                        sl_no=self.safe_int(row[0]) if len(row) > 0 else None,
                        granted_patent_no=row[1].strip() if len(row) > 1 and row[1] else None,
                        date_of_grant=row[2].strip() if len(row) > 2 and row[2] else None,
                        inventors=row[3].strip() if len(row) > 3 and row[3] else None,
                        title=row[4].strip() if len(row) > 4 and row[4] else None,
                        application_number=row[5].strip() if len(row) > 5 and row[5] else None,
                        date_of_publication=row[6].strip() if len(row) > 6 and row[6] else None,
                        filing_institute=row[7].strip() if len(row) > 7 and row[7] else None,
                        abstract=row[8].strip() if len(row) > 8 and row[8] else None,
                    )
                    count += 1
                except Exception as e:
                    self.stdout.write(self.style.WARNING(f'Skipped row: {e}'))
            
            self.stdout.write(self.style.SUCCESS(f'Imported {count} granted patent records'))

    def safe_int(self, value):
        """Safely convert value to integer"""
        try:
            return int(float(str(value).strip())) if value else None
        except (ValueError, TypeError):
            return None
