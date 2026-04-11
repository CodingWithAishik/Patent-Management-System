import csv
from pathlib import Path

from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from patents.models import Copyright, PatentFiled, PatentGranted
from patents.utils.csv_preprocessing import (
    HEADER_MARKERS,
    clean_text,
    compact_row,
    find_header_row,
    is_empty_row,
    is_noise_row,
    normalize_application_number,
    normalize_date_text,
    normalize_multiline_text,
    normalize_publication_status,
    normalize_year,
    row_is_header,
    signature_from_values,
)


class Command(BaseCommand):
    help = 'Import data from CSV files into the database'

    def add_arguments(self, parser):
        parser.add_argument(
            '--diagnostic',
            action='store_true',
            help='Show cleanup diagnostics for excluded rows during import',
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
            help='Fail import if any rows are excluded during cleanup',
        )

    def handle(self, *args, **options):
        self.diagnostic = options.get('diagnostic', False)
        self.diagnostic_limit = max(1, options.get('diagnostic_limit', 10) or 10)
        self.strict_exclusions = options.get('strict_exclusions', False)
        self.total_excluded_rows = 0
        base_dir = Path(settings.BASE_DIR)
        
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

        if self.strict_exclusions and self.total_excluded_rows > 0:
            raise CommandError(
                f'Strict exclusion check failed: {self.total_excluded_rows} row(s) were excluded during cleanup'
            )
        
        self.stdout.write(self.style.SUCCESS('\n\nImport completed successfully!'))
        self.stdout.write(f'Copyrights: {Copyright.objects.count()}')
        self.stdout.write(f'Patents Filed: {PatentFiled.objects.count()}')
        self.stdout.write(f'Patents Granted: {PatentGranted.objects.count()}')

    def load_rows(self, file_path):
        with open(file_path, 'r', encoding='utf-8-sig', newline='') as handle:
            return list(csv.reader(handle))

    def import_copyrights(self, file_path):
        """Import copyright data from CSV"""
        if not Path(file_path).exists():
            self.stdout.write(self.style.ERROR(f'File not found: {file_path}'))
            return
        
        rows = self.load_rows(file_path)
        header_row_idx = find_header_row(rows, HEADER_MARKERS['copyright'])

        if header_row_idx is None:
            self.stdout.write(self.style.ERROR('Could not find copyright header row'))
            return

        diagnostics = self._start_diagnostics('Copyrights', file_path, header_row_idx, len(rows))

        seen_signatures = set()
        count = 0
        skipped = 0

        for row_number, raw_row in enumerate(rows[header_row_idx + 1:], start=header_row_idx + 2):
            if is_empty_row(raw_row):
                self._record_diagnostic(diagnostics, 'empty_rows', row_number, raw_row)
                continue
            if is_noise_row(raw_row):
                self._record_diagnostic(diagnostics, 'noise_rows', row_number, raw_row)
                continue
            if row_is_header(raw_row, HEADER_MARKERS['copyright']):
                self._record_diagnostic(diagnostics, 'header_like_rows', row_number, raw_row)
                continue

            row = compact_row(raw_row, expected_length=6, merge_start=3, tail_length=3)
            if len(row) != 6:
                skipped += 1
                self._record_diagnostic(
                    diagnostics,
                    'structurally_ambiguous_rows',
                    row_number,
                    raw_row,
                    detail=f'compacted length={len(row)} expected=6',
                )
                self.stdout.write(self.style.WARNING(f'Skipped copyright row {row_number}: unexpected structure'))
                continue

            values = [
                self.safe_int(row[0]),
                normalize_year(row[1]),
                clean_text(row[2]),
                normalize_multiline_text(row[3]),
                normalize_multiline_text(row[4]),
                normalize_multiline_text(row[5]),
            ]

            signature = signature_from_values(values)
            if signature in seen_signatures:
                self._record_diagnostic(diagnostics, 'duplicate_rows', row_number, raw_row)
                continue
            seen_signatures.add(signature)

            try:
                Copyright.objects.create(
                    sl_no=values[0],
                    year=values[1],
                    faculty_students=values[2],
                    title=values[3],
                    filing_info=values[4],
                    inventors=values[5],
                )
                count += 1
            except Exception as exc:
                skipped += 1
                self._record_diagnostic(
                    diagnostics,
                    'failed_import_rows',
                    row_number,
                    raw_row,
                    detail=str(exc),
                )
                self.stdout.write(self.style.WARNING(f'Skipped copyright row {row_number}: {exc}'))

        self.stdout.write(self.style.SUCCESS(f'Imported {count} copyright records'))
        if skipped:
            self.stdout.write(self.style.WARNING(f'Skipped {skipped} copyright rows during cleanup'))
        self._emit_diagnostics(diagnostics)

    def import_filed_patents(self, file_path):
        """Import filed patent data from CSV"""
        if not Path(file_path).exists():
            self.stdout.write(self.style.ERROR(f'File not found: {file_path}'))
            return
        
        rows = self.load_rows(file_path)
        header_row_idx = find_header_row(rows, HEADER_MARKERS['filed'])

        if header_row_idx is None:
            self.stdout.write(self.style.ERROR('Could not find filed patent header row'))
            return

        diagnostics = self._start_diagnostics('Filed Patents', file_path, header_row_idx, len(rows))

        seen_signatures = set()
        count = 0
        skipped = 0

        for row_number, raw_row in enumerate(rows[header_row_idx + 1:], start=header_row_idx + 2):
            if is_empty_row(raw_row):
                self._record_diagnostic(diagnostics, 'empty_rows', row_number, raw_row)
                continue
            if is_noise_row(raw_row):
                self._record_diagnostic(diagnostics, 'noise_rows', row_number, raw_row)
                continue
            if row_is_header(raw_row, HEADER_MARKERS['filed']):
                self._record_diagnostic(diagnostics, 'header_like_rows', row_number, raw_row)
                continue

            row = compact_row(raw_row, expected_length=8, merge_start=3, tail_length=4)
            if len(row) != 8:
                skipped += 1
                self._record_diagnostic(
                    diagnostics,
                    'structurally_ambiguous_rows',
                    row_number,
                    raw_row,
                    detail=f'compacted length={len(row)} expected=8',
                )
                self.stdout.write(self.style.WARNING(f'Skipped filed row {row_number}: unexpected structure'))
                continue

            values = [
                self.safe_int(row[0]),
                normalize_date_text(row[1]),
                clean_text(row[2]),
                normalize_multiline_text(row[3]),
                normalize_application_number(row[4]),
                normalize_publication_status(row[5]),
                normalize_multiline_text(row[6]),
                normalize_multiline_text(row[7]),
            ]

            signature = signature_from_values(values)
            if signature in seen_signatures:
                self._record_diagnostic(diagnostics, 'duplicate_rows', row_number, raw_row)
                continue
            seen_signatures.add(signature)

            try:
                PatentFiled.objects.create(
                    sl_no=values[0],
                    date_of_filing=values[1],
                    inventors=values[2],
                    title=values[3],
                    application_number=values[4],
                    date_of_publication=values[5],
                    abstract=values[6],
                    applicant_name=values[7],
                )
                count += 1
            except Exception as exc:
                skipped += 1
                self._record_diagnostic(
                    diagnostics,
                    'failed_import_rows',
                    row_number,
                    raw_row,
                    detail=str(exc),
                )
                self.stdout.write(self.style.WARNING(f'Skipped filed row {row_number}: {exc}'))

        self.stdout.write(self.style.SUCCESS(f'Imported {count} filed patent records'))
        if skipped:
            self.stdout.write(self.style.WARNING(f'Skipped {skipped} filed rows during cleanup'))
        self._emit_diagnostics(diagnostics)

    def import_granted_patents(self, file_path):
        """Import granted patent data from CSV"""
        if not Path(file_path).exists():
            self.stdout.write(self.style.ERROR(f'File not found: {file_path}'))
            return
        
        rows = self.load_rows(file_path)
        header_row_idx = find_header_row(rows, HEADER_MARKERS['granted'])

        if header_row_idx is None:
            self.stdout.write(self.style.ERROR('Could not find granted patent header row'))
            return

        diagnostics = self._start_diagnostics('Granted Patents', file_path, header_row_idx, len(rows))

        seen_signatures = set()
        count = 0
        skipped = 0

        for row_number, raw_row in enumerate(rows[header_row_idx + 1:], start=header_row_idx + 2):
            if is_empty_row(raw_row):
                self._record_diagnostic(diagnostics, 'empty_rows', row_number, raw_row)
                continue
            if is_noise_row(raw_row):
                self._record_diagnostic(diagnostics, 'noise_rows', row_number, raw_row)
                continue
            if row_is_header(raw_row, HEADER_MARKERS['granted']):
                self._record_diagnostic(diagnostics, 'header_like_rows', row_number, raw_row)
                continue

            row = compact_row(raw_row, expected_length=9, merge_start=4, tail_length=5)
            if len(row) != 9:
                skipped += 1
                self._record_diagnostic(
                    diagnostics,
                    'structurally_ambiguous_rows',
                    row_number,
                    raw_row,
                    detail=f'compacted length={len(row)} expected=9',
                )
                self.stdout.write(self.style.WARNING(f'Skipped granted row {row_number}: unexpected structure'))
                continue

            values = [
                self.safe_int(row[0]),
                normalize_multiline_text(row[1]),
                normalize_date_text(row[2]),
                clean_text(row[3]),
                normalize_multiline_text(row[4]),
                normalize_application_number(row[5]),
                normalize_publication_status(row[6]),
                normalize_multiline_text(row[7]),
                normalize_multiline_text(row[8]),
            ]

            signature = signature_from_values(values)
            if signature in seen_signatures:
                self._record_diagnostic(diagnostics, 'duplicate_rows', row_number, raw_row)
                continue
            seen_signatures.add(signature)

            try:
                PatentGranted.objects.create(
                    sl_no=values[0],
                    granted_patent_no=values[1],
                    date_of_grant=values[2],
                    inventors=values[3],
                    title=values[4],
                    application_number=values[5],
                    date_of_publication=values[6],
                    filing_institute=values[7],
                    abstract=values[8],
                )
                count += 1
            except Exception as exc:
                skipped += 1
                self._record_diagnostic(
                    diagnostics,
                    'failed_import_rows',
                    row_number,
                    raw_row,
                    detail=str(exc),
                )
                self.stdout.write(self.style.WARNING(f'Skipped granted row {row_number}: {exc}'))

        self.stdout.write(self.style.SUCCESS(f'Imported {count} granted patent records'))
        if skipped:
            self.stdout.write(self.style.WARNING(f'Skipped {skipped} granted rows during cleanup'))
        self._emit_diagnostics(diagnostics)

    def _start_diagnostics(self, dataset, file_path, header_row_idx, total_rows):
        return {
            'dataset': dataset,
            'file_path': str(file_path),
            'header_row_idx': header_row_idx,
            'total_rows': total_rows,
            'counts': {
                'empty_rows': 0,
                'noise_rows': 0,
                'header_like_rows': 0,
                'structurally_ambiguous_rows': 0,
                'duplicate_rows': 0,
                'failed_import_rows': 0,
            },
            'samples': {
                'empty_rows': [],
                'noise_rows': [],
                'header_like_rows': [],
                'structurally_ambiguous_rows': [],
                'duplicate_rows': [],
                'failed_import_rows': [],
            },
        }

    def _record_diagnostic(self, diagnostics, reason, row_number, raw_row, detail=None):
        diagnostics['counts'][reason] += 1
        if not self.diagnostic:
            return

        samples = diagnostics['samples'][reason]
        if len(samples) < self.diagnostic_limit:
            row_preview = compact_row(raw_row, expected_length=3, merge_start=1, tail_length=1)
            preview_text = clean_text(' | '.join(filter(None, (clean_text(cell) for cell in row_preview))))
            entry = f'row {row_number}'
            if preview_text:
                entry += f' -> {preview_text}'
            if detail:
                entry += f' ({detail})'
            samples.append(entry)

    def _emit_diagnostics(self, diagnostics):
        excluded_this_dataset = sum(diagnostics['counts'].values())
        self.total_excluded_rows += excluded_this_dataset

        if not self.diagnostic:
            return

        self.stdout.write(self.style.WARNING(f"\n[Diagnostics] {diagnostics['dataset']}"))
        self.stdout.write(f"File: {diagnostics['file_path']}")
        self.stdout.write(f"Header row index: {diagnostics['header_row_idx']} (1-based row {diagnostics['header_row_idx'] + 1})")
        self.stdout.write(f"Total CSV rows: {diagnostics['total_rows']}")

        reason_labels = {
            'empty_rows': 'Empty rows',
            'noise_rows': 'Noise/banner rows',
            'header_like_rows': 'Repeated header-like rows',
            'structurally_ambiguous_rows': 'Structurally ambiguous rows',
            'duplicate_rows': 'Duplicate rows by content signature',
            'failed_import_rows': 'Rows failing model insert',
        }

        for reason, label in reason_labels.items():
            count = diagnostics['counts'][reason]
            self.stdout.write(f'- {label}: {count}')
            samples = diagnostics['samples'][reason]
            for sample in samples:
                self.stdout.write(f'  * {sample}')

    def safe_int(self, value):
        """Safely convert value to integer"""
        try:
            text = clean_text(value)
            return int(float(text)) if text else None
        except (ValueError, TypeError):
            return None
