from fastapi import APIRouter, Query
from airtable import get_all_records
from cv_scoring import run_cv_scoring_pipeline

router = APIRouter()


@router.get("/applicants/")
def fetch_applicants():
    raw_records = get_all_records()
    flattened = []

    for rec in raw_records:
        flat = {
            "id": rec.get("id"),
            "createdTime": rec.get("createdTime"),
        }
        fields = rec.get("fields", {})
        for key, value in fields.items():
            if key != "CV":
                flat[key] = value

        flattened.append(flat)

    return flattened


@router.post("/score/cvs/")
def score_multiple_cvs(n: int = Query(..., description="Number of CVs to score")):
    results = run_cv_scoring_pipeline(n)
    return results
