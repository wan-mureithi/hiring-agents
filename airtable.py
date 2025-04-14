from pyairtable import Table
import os
import re
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("AIRTABLE_API_KEY")
BASE_ID = os.getenv("AIRTABLE_BASE_ID")
TABLE_NAME = os.getenv("AIRTABLE_TABLE_NAME")

table = Table(API_KEY, BASE_ID, "applicants")


# Example: extract CV URL using regex
def extract_cv_url(cv_field):
    match = re.search(r"\((https.*?)\)", cv_field)
    return match.group(1) if match else None


def get_all_records():
    """Fetch all records from Airtable table."""
    return table.all()


def get_record(record_id: str):
    """Fetch a specific record by Airtable record ID."""
    return table.get(record_id)


def create_record(data: dict):
    """Create a new record."""
    return table.create(data)


def update_record(record_id: str, data: dict):
    """Update fields in an existing record."""
    return table.update(record_id, data)


def delete_record(record_id: str):
    """Delete a specific record by ID."""
    return table.delete(record_id)


def extract_pdf_url(cv_field: str) -> str:
    """Extracts the link inside parentheses."""
    match = re.search(r"\((https.*?)\)", cv_field)
    return match.group(1) if match else None


def get_candidate_records():
    records = table.all()
    return [
        {
            "id": rec["id"],
            "name": rec["fields"].get("Name"),
            "cv_url": extract_pdf_url(rec["fields"].get("CV", "")),
        }
        for rec in records
        if "CV" in rec["fields"]
    ]
