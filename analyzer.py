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
 
 
MATCH_PROMPT = """You are an expert technical recruiter who specializes in matching candidates to job descriptions.
 
You will be given a job description and a candidate's resume. Analyze how well the resume matches the job and return ONLY a valid JSON object with this exact structure:
 
{
  "match_score": integer between 0 and 100,
  "match_summary": "string — 2-3 sentences summarizing overall fit",
  "matching_skills": ["skills", "the", "candidate", "has", "that", "the", "job", "wants"],
  "missing_skills": ["required", "skills", "completely", "absent", "from", "the", "resume"],
  "irrelevant_skills": ["skills", "on", "resume", "that", "dont", "matter", "for", "this", "role"],
  "strong_points": ["list of 2-3 things the candidate does well for this role"],
  "improvements": ["list of 2-3 specific actionable things to add or fix on the resume for this role"]
}
 
Match score guide:
- 90-100: Extremely strong fit, nearly all required skills present
- 70-89: Good fit, most skills present with minor gaps
- 50-69: Partial fit, some key skills missing
- Below 50: Weak fit, significant skill gaps or wrong background
 
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
            model="gemini-2.5-flash-lite",
            contents=jd_text.strip(),
            config=types.GenerateContentConfig(
                system_instruction=SYSTEM_PROMPT,
                response_mime_type="application/json"
            )
        )
 
        raw = response.text.strip()
 
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
 
 
def match_resume_to_jd(jd_text: str, resume_text: str) -> dict:
    """
    Takes a job description and resume, returns a match analysis.
    Returns a dict with the match result or an error key if something went wrong.
    """
    if not resume_text or len(resume_text.strip()) < 50:
        return {"error": "Resume is too short. Please paste your full resume."}
 
    if not jd_text or len(jd_text.strip()) < 50:
        return {"error": "Job description is too short. Please paste the full posting."}
 
    try:
        contents = f"JOB DESCRIPTION:\n{jd_text.strip()}\n\nRESUME:\n{resume_text.strip()}"
 
        response = client.models.generate_content(
            model="gemini-2.5-flash-lite",
            contents=contents,
            config=types.GenerateContentConfig(
                system_instruction=MATCH_PROMPT,
                response_mime_type="application/json"
            )
        )
 
        raw = response.text.strip()
 
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