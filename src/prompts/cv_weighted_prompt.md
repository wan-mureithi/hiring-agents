You are evaluating a candidate for a **Technical Data Scientist** role. Use the three weighted criteria below.

Assign a score between **0 and 100** for each main criterion independently based on the resume. Then, compute the final weighted score out of 100 using the weights provided.

## Scoring Criteria:

1. **Technical experience** (weight: 60%)
   - Programming ability (especially Python)
   - Experience in analytics, engineering, or AI/data solutions

2. **High Potential and Brightness** (weight: 30%)
   - Analytical mindset
   - Evidence of adaptability, initiative, or curiosity

3. **Social Impact Orientation** (weight: 10%)
   - Motivation to apply data/AI for meaningful social or financial problems

---

## Resume:
{{RESUME_TEXT}}

---

## Output Instructions:
- `final_score` must be a **concrete numeric value** only — not a formula or calculation.
- **You must compute all scores before returning the output.**
- Return a single-line **valid JSON** object only — no markdown or explanation.
- Include a short `"reasoning"` field (1–2 sentences max) based on the scores.

Example structure (note: do NOT copy these exact scores):
```json
{
  "technical_experience": 40,
  "high_potential": 20,
  "social_impact": 4,
  "final_score": 64,
  "reasoning": "The candidate demonstrated strong technical skills but had limited direct experience in social impact."
}