import os
import json
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()

api_key = os.getenv("GOOGLE_API_KEY")

if not api_key:
    raise ValueError("Missing GOOGLE_API_KEY. Check your .env file.")

client = genai.Client(api_key=api_key)

SYSTEM_PROMPT = """You are an expert technical recruiter and career coach who has reviewed thousands of job postings.

When given a job description, you analyze it and return ONLY a valid JSON object with this exact structure:

{
  "role_title": "string — the actual job title",
  "seniority": "string — one of: Intern, Junior, Mid-level, Senior, Staff, Lead",
  "company_signals": "string — 1-2 sentences about what the company seems like based on the JD",
  "required_skills": ["list", "of", "hard", "required", "skills"],
  "nice_to_have_skills": ["list", "of", "preferred", "but", "optional", "skills"],
  "red_flags": ["list of any red flags — e.g. vague comp, too many requirements, no mention of team size"],
  "legitimacy_score": integer between 0 and 100,
  "legitimacy_reason": "string — 1-2 sentences explaining the score",
  "ats_keywords": ["top", "keywords", "to", "include", "on", "a", "resume"],
  "one_line_summary": "string — one punchy sentence summarizing this role"
}

Legitimacy score guide:
- 90-100: Clear role, real company signals, reasonable requirements, compensation mentioned
- 70-89: Decent posting, minor vagueness, comp missing but otherwise solid
- 50-69: Some red flags — vague, laundry list of requirements, or feels templated
- Below 50: Ghost job vibes, unrealistic expectations, or major missing info

Return ONLY the JSON. No explanation, no markdown, no backticks."""
 
 
def analyze_job_description(jd_text: str) -> dict:
    """
    Takes a raw job description string and returns structured analysis.
    Returns a dict with the analysis or an error key if something went wrong.
    """
    if not jd_text or len(jd_text.strip()) < 50:
        return {"error": "Job description is too short. Please paste the full posting."}

    try:
        response = client.models.generate_content(
            model="gemini-3.1-flash-lite-preview",
            contents=jd_text.strip(),
            config=types.GenerateContentConfig(
                system_instruction=SYSTEM_PROMPT,
                response_mime_type="application/json"
            )
        )

        raw = response.text.strip()

        # Extra safety in case the model adds markdown fences anyway
        if raw.startswith("```"):
            raw = raw.replace("```json", "").replace("```", "").strip()

        return json.loads(raw)

    except json.JSONDecodeError:
        return {
            "error": "The AI returned an unexpected format. Try again.",
            "raw_response": raw if "raw" in locals() else None
        }

    except Exception as e:
        return {"error": f"Something went wrong: {str(e)}"}