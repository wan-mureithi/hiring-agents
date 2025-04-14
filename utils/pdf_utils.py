import re
import io
import requests
from typing import List
from PyPDF2 import PdfReader
from airtable import get_all_records
from utils.preprocess import clean_cv_text


def download_pdf(url: str) -> io.BytesIO:
    """Downloads the PDF and returns it as a BytesIO stream."""
    response = requests.get(url)
    response.raise_for_status()
    return io.BytesIO(response.content)


def extract_resume_url(resume_field: list) -> str:
    """Extract the direct download URL from the Airtable attachment field."""
    if isinstance(resume_field, list) and resume_field:
        return resume_field[0].get("url")
    return None


def extract_text_from_pdf(content: io.BytesIO) -> str:
    reader = PdfReader(content)
    print("READER", reader)
    text = []
    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text.append(page_text.strip())
    return "\n".join(text)


def test_first_cv():
    # Only get the first record from Airtable
    record = get_all_records()[0]

    fields = record.get("fields", {})
    resume_field = fields.get("resume")

    if not resume_field:
        print(f"❌ No CV field for: {fields.get('Name')}")
        return

    resume_url = extract_resume_url(resume_field)
    if not resume_url:
        print(f"❌ No valid link in CV field for: {fields.get('Name')}")
        return

    print(f"🔗 Testing CV for: {fields.get('Name')}")

    try:
        content = download_pdf(resume_url)
        # print("\n✅ CONTENT:", content)
        raw_text = extract_text_from_pdf(content)
        # print("\n✅ RAW:", raw_text)
        cleaned_text = clean_cv_text(raw_text)
        # print("\n✅ CLEAN:", cleaned_text)

        print("\n✅ CLEANED TEXT (first 500 chars):")
        print(cleaned_text[:500])

    except Exception as e:
        print(f"❌ Failed to process {fields.get('Name')}: {e}")
