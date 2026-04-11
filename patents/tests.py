from django.test import TestCase
from django.urls import reverse

from patents.models import IPCategory, IntellectualProperty

from patents.utils.csv_preprocessing import (
	HEADER_MARKERS,
	compact_row,
	find_header_row,
	normalize_application_number,
	normalize_date_text,
	normalize_publication_status,
	normalize_year,
	row_is_header,
)


class CSVPreprocessingTests(TestCase):
	def test_find_header_row_ignores_title_rows(self):
		rows = [
			["Details of Patent Filing inIIEST, Shibpur"],
			["", "", "Sl. No.", "Date of Filing", "Title of Patent", "Application Number"],
			["1", "17.06.2025", "Example", "Title", "202531058128 A"],
		]

		self.assertEqual(find_header_row(rows, HEADER_MARKERS["filed"]), 1)

	def test_row_is_header_detects_repeated_header(self):
		row = ["Sl. No.", "Date of Grant", "Granted Patent No.", "Title of Patent"]

		self.assertTrue(row_is_header(row, HEADER_MARKERS["granted"]))

	def test_compact_row_merges_overflow_into_middle_field(self):
		row = [
			"1",
			"2024",
			"Inventor A",
			"Title part one",
			"Title part two",
			"202531058128 A",
			"20.06.2025",
			"Abstract text",
			"Applicant",
		]

		compacted = compact_row(row, expected_length=8, merge_start=3, tail_length=4)

		self.assertEqual(len(compacted), 8)
		self.assertEqual(compacted[3], "Title part one Title part two")

	def test_date_normalization_covers_mixed_formats(self):
		self.assertEqual(normalize_date_text("17.06.2025"), "17/06/2025")
		self.assertEqual(normalize_date_text("19th July 2024"), "19/07/2024")
		self.assertEqual(normalize_date_text("Dec 2024"), "Dec 2024")

	def test_application_number_normalization_strips_date_suffix(self):
		self.assertEqual(
			normalize_application_number("MOIL Limited, Govt. of India. 202021008379 dated 27.02.2020"),
			"202021008379",
		)
		self.assertEqual(
			normalize_application_number("US17/434,688 date 28/02/2022"),
			"US17/434,688",
		)

	def test_publication_status_normalization(self):
		self.assertEqual(normalize_publication_status("Not Yet published"), "Not yet published")
		self.assertEqual(normalize_publication_status("20.06.2025"), "20/06/2025")

	def test_year_normalization_keeps_four_digit_year(self):
		self.assertEqual(normalize_year("Year 2024"), "2024")


class DynamicIPValidationTests(TestCase):
	def setUp(self):
		self.category = IPCategory.objects.create(
			name="Trademarks",
			description="Dynamic category validation tests",
			field_definitions=[
				{"name": "title", "label": "Title", "type": "text", "required": True},
				{"name": "year", "label": "Year", "type": "number", "required": False},
				{"name": "filing_date", "label": "Filing Date", "type": "date", "required": False},
				{
					"name": "status",
					"label": "Status",
					"type": "select",
					"required": False,
					"options": ["Filed", "Granted"],
				},
			],
		)

	def test_ip_create_rejects_missing_required_field(self):
		url = reverse("patents:ip_create", kwargs={"category_slug": self.category.slug})

		response = self.client.post(
			url,
			{
				"title": "",
				"year": "2026",
			},
		)

		self.assertEqual(response.status_code, 200)
		self.assertContains(response, "Title is required.")
		self.assertEqual(IntellectualProperty.objects.count(), 0)

	def test_ip_create_rejects_invalid_number_date_and_select(self):
		url = reverse("patents:ip_create", kwargs={"category_slug": self.category.slug})

		response = self.client.post(
			url,
			{
				"title": "Example IP",
				"year": "twenty",
				"filing_date": "2026-13-40",
				"status": "Published",
			},
		)

		self.assertEqual(response.status_code, 200)
		self.assertContains(response, "Year must be a valid number.")
		self.assertContains(response, "Filing Date must be a valid date (YYYY-MM-DD).")
		self.assertContains(response, "Status must be one of the allowed options.")
		self.assertEqual(IntellectualProperty.objects.count(), 0)

	def test_ip_create_accepts_valid_payload(self):
		url = reverse("patents:ip_create", kwargs={"category_slug": self.category.slug})

		response = self.client.post(
			url,
			{
				"title": "Advanced Trademark Filing",
				"year": "2026",
				"filing_date": "2026-04-11",
				"status": "Filed",
			},
		)

		self.assertEqual(response.status_code, 302)
		self.assertEqual(IntellectualProperty.objects.count(), 1)

		created = IntellectualProperty.objects.first()
		self.assertEqual(created.data.get("title"), "Advanced Trademark Filing")
		self.assertEqual(created.data.get("year"), "2026")
		self.assertEqual(created.data.get("filing_date"), "2026-04-11")
		self.assertEqual(created.data.get("status"), "Filed")


class CategorySchemaValidationTests(TestCase):
	def test_category_create_rejects_duplicate_field_names(self):
		url = reverse("patents:category_create")

		response = self.client.post(
			url,
			{
				"name": "Designs",
				"description": "Schema test",
				"field_name_0": "patent_id",
				"field_label_0": "Patent ID",
				"field_type_0": "text",
				"field_name_1": "Patent_ID",
				"field_label_1": "Duplicate Patent ID",
				"field_type_1": "number",
			},
		)

		self.assertEqual(response.status_code, 200)
		self.assertContains(response, "Duplicate field name")
		self.assertEqual(IPCategory.objects.count(), 0)

	def test_category_create_rejects_select_without_options(self):
		url = reverse("patents:category_create")

		response = self.client.post(
			url,
			{
				"name": "Technology Transfer",
				"description": "Schema test",
				"field_name_0": "status",
				"field_label_0": "Status",
				"field_type_0": "select",
				"field_options_0": "",
			},
		)

		self.assertEqual(response.status_code, 200)
		self.assertContains(response, "Select fields must define at least one option.")
		self.assertEqual(IPCategory.objects.count(), 0)

	def test_category_create_rejects_invalid_field_name(self):
		url = reverse("patents:category_create")

		response = self.client.post(
			url,
			{
				"name": "Geographical Indications",
				"description": "Schema test",
				"field_name_0": "123 bad name",
				"field_label_0": "Bad",
				"field_type_0": "text",
			},
		)

		self.assertEqual(response.status_code, 200)
		self.assertContains(response, "is invalid. Use letters, numbers, underscores, and start with a letter.")
		self.assertEqual(IPCategory.objects.count(), 0)

	def test_category_create_accepts_valid_schema(self):
		url = reverse("patents:category_create")

		response = self.client.post(
			url,
			{
				"name": "Industrial Designs",
				"description": "Design registry",
				"field_name_0": "design_no",
				"field_label_0": "Design Number",
				"field_type_0": "text",
				"field_required_0": "on",
				"field_name_1": "status",
				"field_label_1": "Status",
				"field_type_1": "select",
				"field_options_1": "Filed, Granted",
			},
		)

		self.assertEqual(response.status_code, 302)
		self.assertEqual(IPCategory.objects.count(), 1)

		category = IPCategory.objects.first()
		self.assertEqual(category.name, "Industrial Designs")
		self.assertEqual(len(category.field_definitions), 2)
		self.assertEqual(category.field_definitions[1]["options"], ["Filed", "Granted"])
