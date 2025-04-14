from crewai import Crew, Agent, Task
from utils.llm_wrapper import query_llm
from airtable import get_all_records
from utils.pdf_utils import download_pdf, extract_text_from_pdf, extract_resume_url
import io
from pathlib import Path


def load_cv_prompt(cv_text: str) -> str:
    template_path = Path("src/hiring_agents/config/simple_prompt.md")
    template = template_path.read_text()
    print("TEMPLATE", template)
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
