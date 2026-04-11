import re
import unicodedata
from datetime import datetime


HEADER_MARKERS = {
    "copyright": ("sl no", "year", "title of copy rights"),
    "filed": ("sl no", "date of filing", "application number", "title of patent"),
    "granted": ("sl no", "granted patent no", "date of grant", "title of patent"),
}


_FULL_DATE_FORMATS = (
    "%d/%m/%Y",
    "%d-%m-%Y",
    "%d.%m.%Y",
    "%Y-%m-%d",
    "%d/%m/%y",
    "%d-%m-%y",
    "%d.%m.%y",
    "%d %B %Y",
    "%d %b %Y",
    "%d %B, %Y",
    "%d %b, %Y",
)

_MONTH_YEAR_FORMATS = (
    "%B %Y",
    "%b %Y",
    "%B, %Y",
    "%b, %Y",
)


def clean_text(value):
    if value is None:
        return None

    text = unicodedata.normalize("NFKC", str(value))
    text = text.replace("\xa0", " ")
    text = text.replace("\u200b", "")
    text = text.replace("Â", "")
    text = text.replace("\r", " ").replace("\n", " ")
    text = re.sub(r"\s+", " ", text).strip()
    return text or None


def normalize_header_cell(value):
    text = clean_text(value)
    if not text:
        return ""
    text = text.lower()
    text = re.sub(r"[^a-z0-9]+", " ", text)
    return re.sub(r"\s+", " ", text).strip()


def row_is_header(row, markers):
    normalized = {normalize_header_cell(cell) for cell in row if clean_text(cell)}
    return all(marker in normalized for marker in markers)


def find_header_row(rows, markers):
    best_index = None
    best_score = 0
    for index, row in enumerate(rows):
        normalized = {normalize_header_cell(cell) for cell in row if clean_text(cell)}
        score = sum(1 for marker in markers if marker in normalized)
        if score > best_score:
            best_index = index
            best_score = score
    if best_score >= 2:
        return best_index
    return None


def normalize_year(value):
    text = clean_text(value)
    if not text:
        return None
    match = re.search(r"\b(19|20)\d{2}\b", text)
    if match:
        return match.group(0)
    return text


def normalize_date_text(value):
    text = clean_text(value)
    if not text:
        return None

    text = re.sub(r"(\d{1,2})(st|nd|rd|th)\b", r"\1", text, flags=re.IGNORECASE)

    for date_format in _FULL_DATE_FORMATS:
        try:
            return datetime.strptime(text, date_format).strftime("%d/%m/%Y")
        except ValueError:
            continue

    for date_format in _MONTH_YEAR_FORMATS:
        try:
            return datetime.strptime(text, date_format).strftime("%b %Y")
        except ValueError:
            continue

    if re.fullmatch(r"\b(19|20)\d{2}\b", text):
        return text

    return text


def normalize_publication_status(value):
    text = clean_text(value)
    if not text:
        return None
    if re.search(r"not\s+yet\s+published", text, flags=re.IGNORECASE):
        return "Not yet published"
    return normalize_date_text(text)


def normalize_application_number(value):
    text = clean_text(value)
    if not text:
        return None

    if re.search(r"not\s+yet\s+published", text, flags=re.IGNORECASE):
        return "Not yet published"

    text = re.split(r"\bdated?\b", text, maxsplit=1, flags=re.IGNORECASE)[0].strip(" ,;-")
    if "." in text:
        tail = text.rsplit(".", 1)[-1].strip()
        if tail and any(char.isdigit() for char in tail):
            text = tail

    return re.sub(r"\s+", " ", text).strip(" ,;") or None


def normalize_multiline_text(value):
    text = clean_text(value)
    if not text:
        return None
    text = re.sub(r"\s*\n\s*", "; ", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def is_empty_row(row):
    return not any(clean_text(cell) for cell in row)


def is_noise_row(row):
    text = " ".join(filter(None, (clean_text(cell) for cell in row)))
    if not text:
        return True
    lowered = text.lower()
    return lowered.startswith("details of ") or lowered in {
        "details of copy rights of iiest, shibpur",
        "details of patent filing iniiest, shibpur",
        "details of granted patents in iiest, shibpur",
    }


def signature_from_values(values):
    return tuple(clean_text(value) or "" for value in values)


def compact_row(row, expected_length, merge_start, tail_length):
    cleaned = list(row)
    if len(cleaned) < expected_length:
        cleaned.extend([None] * (expected_length - len(cleaned)))
        return cleaned

    if len(cleaned) == expected_length:
        return cleaned

    head = cleaned[:merge_start]
    middle = cleaned[merge_start:len(cleaned) - tail_length]
    tail = cleaned[len(cleaned) - tail_length:]

    merged_middle = clean_text(" ".join(filter(None, (clean_text(cell) for cell in middle))))
    return head + [merged_middle] + tail