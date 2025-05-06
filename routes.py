from fastapi import APIRouter, Query, HTTPException
from airtable import get_all_records, get_record, update_record
from cv_scoring import process_single_record, run_cv_scoring_pipeline
from utils.pairwise_ranking import run_elo_match
from pydantic import BaseModel
from datetime import datetime, timedelta, timezone

router = APIRouter()


class HumanScore(BaseModel):
    user_rating: float
    user_reasoning: str


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


@router.post("/score/human/{record_id}")
def score_by_human(record_id: str, payload: HumanScore):
    record = get_record(record_id)
    if not record or "fields" not in record:
        raise HTTPException(status_code=404, detail="Record not found")

    update_payload = {
        "User rating": payload.user_rating,
        "User reasoning": payload.user_reasoning,
    }

    updated = update_record(record_id, update_payload)
    return {"message": "Record updated successfully", "updated": updated}


@router.get("/metrics")
def get_metrics():
    records = get_all_records()

    now = datetime.now(timezone.utc)
    days_ago_30 = now - timedelta(days=30)
    days_ago_60 = now - timedelta(days=60)

    def parse_applied_date(record):
        try:
            date_str = record.get("fields", {}).get("Date applied")
            if not date_str:
                return None
            return datetime.strptime(date_str, "%Y-%m-%d").replace(tzinfo=timezone.utc)
        except Exception:
            return None

    recent_records = [
        r for r in records if (d := parse_applied_date(r)) and d >= days_ago_30
    ]
    past_records = [
        r
        for r in records
        if (d := parse_applied_date(r)) and days_ago_60 <= d < days_ago_30
    ]

    def percentage_change(current, previous):
        if previous == 0:
            if current == 0:
                return "-", "neutral"
            return "-", "up"
        change = ((current - previous) / previous) * 100
        direction = "up" if change > 0 else "down" if change < 0 else "neutral"
        return f"{change:+.1f}%", direction

    # Total applicants
    total_now = len(recent_records)
    total_before = len(past_records)
    trend1, dir1 = percentage_change(total_now, total_before)

    # AI-scored candidates
    def is_ai_scored(r):
        return "CV rating" in r.get("fields", {})

    ai_now = sum(1 for r in recent_records if is_ai_scored(r))
    ai_before = sum(1 for r in past_records if is_ai_scored(r))
    trend2, dir2 = percentage_change(ai_now, ai_before)

    # Top candidates
    def is_top(r):
        try:
            fields = r.get("fields", {})
            return (
                float(fields.get("Elo score", 0)) > 1100
                and float(fields.get("CV rating", 0)) >= 70
            )
        except:
            return False

    top_now = sum(1 for r in recent_records if is_top(r))
    top_before = sum(1 for r in past_records if is_top(r))
    trend3, dir3 = percentage_change(top_now, top_before)

    # Pending human review
    def is_pending(r):
        fields = r.get("fields", {})
        return "User rating" not in fields

    pending_now = sum(1 for r in recent_records if is_pending(r))
    pending_before = sum(1 for r in past_records if is_pending(r))
    trend4, dir4 = percentage_change(pending_now, pending_before)

    return [
        {
            "label": "Total Applicants",
            "value": total_now,
            "trend": trend1,
            "direction": dir1,
            "status": "Trending upward" if dir1 == "up" else "Slowing down",
            "description": "New resumes received in the last 30 days",
        },
        {
            "label": "AI-Scored Candidates",
            "value": ai_now,
            "trend": trend2,
            "direction": dir2,
            "status": "Scoring coverage improving"
            if dir2 == "up"
            else "Scoring coverage slowing",
            "description": "LLM-rated resumes based on criteria",
        },
        {
            "label": "Top Candidates",
            "value": top_now,
            "trend": trend3,
            "direction": dir3,
            "status": "Ready for review"
            if dir3 == "up"
            else "Top candidates declining",
            "description": "Applicants with Elo score > 1100 and CV rating ≥ 70%",
        },
        {
            "label": "Pending Human Review",
            "value": pending_now,
            "trend": trend4,
            "direction": dir4,
            "status": "Queue clearing slowly" if dir4 == "down" else "Queue growing",
            "description": "Awaiting manual evaluator feedback",
        },
    ]
