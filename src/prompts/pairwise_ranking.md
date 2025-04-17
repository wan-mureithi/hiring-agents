You are comparing two applicants for a **Technical Data Scientist** role at a social impact-oriented financial tech company.

Your job is to evaluate both candidates based on the criteria below and decide who is the better fit. Use the evaluation criteria provided and base your decision only on the information in their resumes.

---

## Evaluation Criteria

1. **Technical Experience**
   - Programming ability (especially Python)
   - Data analytics, software engineering, or AI-driven solution design

2. **High Potential and Brightness**
   - Analytical thinking, curiosity, initiative, and learning agility

3. **Finance or Social Impact Experience**
   - Experience or demonstrated interest in the finance or social sectors

4. **Additional Desirable Criteria**
   - JavaScript or frontend development
   - Generative AI project work
   - Awareness or practice of Responsible AI or Ethics in AI

---

## Candidate A

{{RESUME_A}}

---

## Candidate B

{{RESUME_B}}

---

## Output Format

Return a **valid JSON object** using this structure:

```json
{
   "reasoning": {
      "technical_experience": "Applicant A is better because ...",
      "high_potential": "Applicant B is better because ...",
      "finance_experience": "Applicant A is better because ...",
      "additional_criteria": "Applicant B has more of the additional desirable criteria because ...",
      "overall": "Weighing the scores from these categories, Applicant A is overall a better fit. In case of tie, technical experience is used as the deciding factor."
   },
   "winner": "A"
}
