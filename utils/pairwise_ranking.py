import json
from src.algorithms.elo import EloRanking
from pathlib import Path
from airtable import update_record, get_all_records
import random

from utils.llm_wrapper import query_llm
from utils.pdf_utils import download_pdf, extract_resume_url, extract_text_from_pdf


def get_eligible_applicants():
    records = get_all_records()
    eligible = []

    for rec in records:
        fields = rec.get("fields", {})
        if fields.get("Status") == "Applied":
            elo_raw = fields.get("Elo score", 1000)
            elo_clean = (
                int(str(elo_raw).replace(",", ""))
                if isinstance(elo_raw, str)
                else elo_raw
            )
            eligible.append(
                {
                    "id": rec["id"],
                    "name": fields.get("Name", "Unnamed"),
                    "resume": fields.get("resume", []),
                    "elo": elo_clean,
                    "n_games": fields.get("No of games", 0),
                }
            )

    return eligible


def select_random_pair(eligible):
    # print("ELL", eligible)
    if len(eligible) < 2:
        return None, None
    return random.sample(eligible, 2)


def load_pairwise_prompt(text_a: str, text_b: str) -> str:
    path = Path("src/prompts/pairwise_ranking.md")
    template = path.read_text()
    return template.replace("{{RESUME_A}}", text_a).replace("{{RESUME_B}}", text_b)


def choose_winner(app1, app2):
    # Step 1: Extract resume text
    resume_url_a = extract_resume_url(app1.get("resume"))
    resume_url_b = extract_resume_url(app2.get("resume"))

    text_a = extract_text_from_pdf(download_pdf(resume_url_a))
    text_b = extract_text_from_pdf(download_pdf(resume_url_b))

    # Step 2: Build prompt and send to LLM
    prompt = load_pairwise_prompt(text_a, text_b)
    system = "You are an AI HR assistant comparing two candidates for a data role."

    response = query_llm(prompt, system_prompt=system)

    try:
        result = json.loads(response)
        winner = app1 if result["winner"].strip().upper() == "A" else app2
        loser = app2 if result["winner"].strip().upper() == "A" else app1
        print("STUFFF", winner, loser, result["reasoning"])
        return winner, loser, result["reasoning"]
    except Exception as e:
        print("⚠️ Failed to parse LLM response:", e)
        print("LLM Response:", response)
        return app1, app2, "Fallback: Could not parse LLM output"


def run_elo_match():
    eligible = get_eligible_applicants()
    app1, app2 = select_random_pair(eligible)
    print("APPP", app1, app2)
    if not app1 or not app2:
        return {"message": "Not enough candidates for Elo ranking"}

    winner, loser, reasoning = choose_winner(app1, app2)
    ratings = {
        winner["id"]: {"elo": winner["elo"], "n_games": winner["n_games"]},
        loser["id"]: {"elo": loser["elo"], "n_games": loser["n_games"]},
    }

    updated = EloRanking().update_ratings(winner["id"], loser["id"], ratings)

    for record_id, values in updated.items():
        update_record(
            record_id,
            {
                "Elo score": round(values["elo"]),
                "No of games": values["n_games"],
                "Status": "Elo ranked",
            },
        )

    return {
        "message": f'Comparing "{winner["name"]}" and "{loser["name"]}"',
        "winner": winner["name"],
        "loser": loser["name"],
        "reasoning": reasoning,
        "updated_scores": updated,
    }
