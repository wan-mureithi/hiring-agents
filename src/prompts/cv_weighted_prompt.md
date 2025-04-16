You are evaluating a candidate for a **Technical Data Scientist** role. Use the three weighted criteria below.

Assign a score between **0 and 100** for each main criterion independently based on the resume. Then, compute the final weighted score out of 100 using the weights provided.

## Scoring Criteria:

1. **Technical experience** (weight: 60%)
   - Programming ability (especially Python)
   - Experience in analytics, engineering, or AI/data solutions

2. **High Potential and Brightness** (weight: 20%)
   - Analytical mindset
   - Evidence of adaptability, initiative, or curiosity

3. **Social Impact Orientation** (weight: 20%)
   - Motivation to apply data/AI for meaningful social or financial problems

---

## Resume:
{{RESUME_TEXT}}

---

## Output Instructions:
- `final_score` must be a **weighted sum** of the 3 scores, max value **100**
- Return a single-line **valid JSON** object only — no markdown or explanation
- Include a short `"reasoning"` field (1–2 sentences max) based on the scores

Here is a JSON object example:

```json
{
  "technical_experience": 75,
  "high_potential": 60,
  "social_impact": 40,
  "final_score": 66,
  "reasoning": "The candidate demonstrated strong technical skills but had limited direct experience in social impact."
}
