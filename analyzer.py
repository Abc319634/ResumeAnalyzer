import json
import re
from google import genai
from google.genai import types


def analyze_with_ai(resume_text: str, opportunity_text: str, opportunity_type: str, api_key: str) -> dict:
    """
    Use Google Gemini to intelligently analyze resume vs opportunity.
    Returns a structured dict with score, matched_skills, missing_skills, suggestions.
    """
    client = genai.Client(api_key=api_key)

    prompt = f"""
You are an expert career counselor and resume analyst. Analyze the following resume against the opportunity description and return a structured JSON response.

OPPORTUNITY TYPE: {opportunity_type}

--- RESUME ---
{resume_text[:4000]}

--- OPPORTUNITY DESCRIPTION ---
{opportunity_text[:3000]}

Analyze the match and return ONLY a valid JSON object with exactly this structure (no markdown, no explanation, just raw JSON):

{{
    "score": <integer 0-100 representing compatibility percentage>,
    "matched_skills": ["skill1", "skill2", ...],
    "missing_skills": ["skill1", "skill2", ...],
    "strengths": ["strength point 1", "strength point 2", ...],
    "suggestions": ["actionable suggestion 1", "actionable suggestion 2", ...],
    "summary": "<2-3 sentence summary explaining the score and overall fit>"
}}

Rules:
- score should reflect how well the resume matches the opportunity requirements
- matched_skills: specific skills/technologies/qualities found in BOTH resume and opportunity
- missing_skills: specific skills/technologies mentioned in opportunity but NOT in resume
- strengths: what the candidate does well relative to this opportunity
- suggestions: specific, actionable improvements the candidate should make
- Be honest and realistic - don't inflate the score
- For {opportunity_type}: {"focus on projects and technologies" if opportunity_type == "Hackathon" else "focus on domain experience and proven impact" if opportunity_type == "Job" else "focus on technical skills and learning potential" if opportunity_type == "Internship" else "focus on teamwork and initiative" if opportunity_type == "College Committee" else "focus on problem-solving and technical skills"}
"""

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
        )
        raw = response.text.strip()

        # Strip markdown code blocks if present
        raw = re.sub(r"^```(?:json)?\s*", "", raw)
        raw = re.sub(r"\s*```$", "", raw)

        data = json.loads(raw)

        return {
            "score":          int(data.get("score", 50)),
            "matched_skills": ", ".join(data.get("matched_skills", [])),
            "missing_skills": ", ".join(data.get("missing_skills", [])),
            "strengths":      data.get("strengths", []),
            "suggestions":    data.get("suggestions", []),
            "summary":        data.get("summary", ""),
            "error":          None,
        }

    except json.JSONDecodeError as e:
        # Try to salvage if JSON is malformed
        return {
            "score":          40,
            "matched_skills": "",
            "missing_skills": "",
            "strengths":      [],
            "suggestions":    ["Could not parse AI response. Please try again."],
            "summary":        "Analysis failed.",
            "error":          f"JSON parse error: {e}",
        }
    except Exception as e:
        # Catch quota/rate-limits and SDK errors safely
        msg = str(e)
        if "RESOURCE_EXHAUSTED" in msg or "429" in msg or "Quota exceeded" in msg:
            return {"error": "Google API Quota Exceeded. The free tier limits were hit or your region restricts access. Clear the API key in Settings to use Keyword Mode."}
        elif "NOT_FOUND" in msg or "404" in msg:
             return {"error": f"API Model not found or deprecated for this key. {msg}"}
        return {"error": f"AI Parsing failed: {msg}"}


# ── Fallback: keyword-based (used if no API key) ─────────────────────────────
SKILLS_DB = [
    "python", "java", "javascript", "typescript", "c++", "c#", "ruby", "php",
    "swift", "kotlin", "go", "rust", "r", "matlab", "scala", "html", "css",
    "react", "angular", "vue", "svelte", "tailwind", "bootstrap", "next.js",
    "node.js", "node", "express", "django", "flask", "fastapi", "spring",
    "sql", "mysql", "postgresql", "sqlite", "mongodb", "redis", "firebase",
    "aws", "azure", "gcp", "docker", "kubernetes", "git", "github", "linux",
    "machine learning", "deep learning", "data science", "data analysis",
    "artificial intelligence", "nlp", "tensorflow", "pytorch", "keras",
    "pandas", "numpy", "scikit-learn", "tableau", "power bi", "excel",
    "android", "ios", "react native", "flutter",
    "communication", "leadership", "teamwork", "problem solving",
    "project management", "agile", "scrum", "time management",
]


def analyze_fallback(resume_data: dict, opportunity_text: str, opportunity_type: str) -> dict:
    parts = [resume_data.get(k, "") or "" for k in
             ["content", "skills", "education", "projects", "experience", "certifications"]]
    full_resume = " ".join(parts).lower()
    full_opp    = opportunity_text.lower()

    matched = [s for s in SKILLS_DB if s in full_opp and s in full_resume]
    missing = [s for s in SKILLS_DB if s in full_opp and s not in full_resume]

    r_words = set(re.findall(r"[a-z]{3,}", full_resume))
    o_words = set(re.findall(r"[a-z]{3,}", full_opp))
    overlap = len(r_words & o_words) / max(len(o_words), 1)
    score   = min(int(overlap * 100) + min(len(matched) * 5, 30), 95)
    score   = max(score, 5)

    suggestions = []
    if missing:
        suggestions.append(f"Add these skills to your resume: {', '.join(missing[:5])}")
    if not matched:
        suggestions.append("Your resume doesn't clearly reflect the skills in this opportunity.")
    suggestions.append("Add an AI API key in Settings for smarter, more accurate analysis.")

    return {
        "score":          score,
        "matched_skills": ", ".join(matched),
        "missing_skills": ", ".join(missing[:10]),
        "strengths":      [],
        "suggestions":    suggestions,
        "summary":        f"Basic keyword analysis: {len(matched)} matching skills found.",
        "error":          None,
    }
