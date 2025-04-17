from fastapi import APIRouter, Query, HTTPException
from airtable import get_all_records, get_record
from cv_scoring import process_single_record, run_cv_scoring_pipeline
from utils.pairwise_ranking import run_elo_match

router = APIRouter()


@router.get("/applicants")
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


@router.post("/score/cvs")
def score_multiple_cvs(n: int = Query(..., description="Number of CVs to score")):
    results = run_cv_scoring_pipeline(n)
    return results


@router.post("/score/cv/{record_id}")
def score_single_cv(record_id: str):
    record = get_record(record_id)
    print("RECORD: ", record)
    if not record or "fields" not in record:
        raise HTTPException(status_code=404, detail="Record not found")

    result = process_single_record(record)
    return result


@router.post("/elo/rank/random")
def rank_random_pair():
    result = run_elo_match()
    return result
