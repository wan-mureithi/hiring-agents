from crewai import Crew, Agent, Task
from utils.llm_wrapper import query_llm
from airtable import get_all_records, update_record
from utils.pdf_utils import download_pdf, extract_text_from_pdf, extract_resume_url
import io
from pathlib import Path
import json


def load_cv_prompt(cv_text: str) -> str:
    # template_path = Path("src/hiring_agents/config/simple_prompt.md")
    template_path = Path("src/prompts/cv_weighted_prompt.md")
    template = template_path.read_text()
    return template.replace("{{RESUME_TEXT}}", cv_text)


# Simulate config (or load from YAML if using CrewBase)
def run_cv_scoring_pipeline(n=2):
    records = get_all_records()[:n]
    processed = []

    for rec in records:
        fields = rec.get("fields", {})
        name = fields.get("Name", "Unnamed")
        resume_field = fields.get("resume", [])
        pdf_url = extract_resume_url(resume_field)

        if not pdf_url:
            continue

        try:
            content = download_pdf(pdf_url)
            cv_text = extract_text_from_pdf(content)
            # print("CV textt: ", cv_text)
            prompt = load_cv_prompt(cv_text)
            print("CV PROMPT: ", prompt)
            system_prompt = "You are an expert AI HR assistant helping screen resumes."

            llm_response = query_llm(prompt=prompt.strip(), system_prompt=system_prompt)
            processed.append({"name": name, "score_response": llm_response})

        except Exception as e:
            processed.append({"name": name, "error": str(e)})

    return processed


def process_single_record(record: dict):
    fields = record.get("fields", {})
    airtable_id = record.get("id")
    name = fields.get("Name", "Unnamed")
    resume_field = fields.get("resume", [])
    pdf_url = extract_resume_url(resume_field)

    if not pdf_url:
        return {"id": airtable_id, "error": "Missing resume file"}

    try:
        content = download_pdf(pdf_url)
        cv_text = extract_text_from_pdf(content)

        # criteria = get_criteria()
        prompt = load_cv_prompt(
            cv_text
        )  # prompt = build_weighted_prompt(cv_text, criteria)
        system_prompt = "You are as strict AI HR assistant evaluating resumes independently. Give a score based on the criteria provided."

        llm_output = query_llm(prompt, system_prompt)
        parsed = json.loads(llm_output)

        final_score = parsed.get("final_score")
        print("SCORE>>>", final_score)
        reasoning = parsed.get("reasoning", "No reasoning provided.")

        update_record(
            airtable_id,
            {
                "CV rating": f"{final_score}%",
                "AI reasoning": reasoning,
                "Status": "AI scored",
            },
        )

        return {
            "id": airtable_id,
            "name": name,
            "cv_rating": final_score,
            "reasoning": reasoning,
            "status": "AI scored",
        }

    except Exception as e:
        return {"id": airtable_id, "error": str(e)}
