import os

from dotenv import load_dotenv
from google import genai


# =====================================================
# LOAD API KEY
# =====================================================

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError(
        "GEMINI_API_KEY not found. "
        "Please check your .env file."
    )


# =====================================================
# CREATE GEMINI CLIENT
# =====================================================

client = genai.Client(api_key=api_key)


# =====================================================
# GENERATE AI RESPONSE
# =====================================================

def generate_ai_response(prompt):

    try:

        response = client.models.generate_content(
            model="gemini-3.6-flash",
            contents=prompt
        )

        if response.text:
            return response.text

        return "No response was generated."

    except Exception as e:

        return f"AI Error: {e}"


# =====================================================
# IMPROVE PROFESSIONAL SUMMARY
# =====================================================

def improve_summary(text):

    prompt = f"""
You are a professional resume writer.

Rewrite the following professional summary.

Requirements:
- Make it professional
- Make it concise
- Make it ATS-friendly
- Use strong professional language
- Correct grammar and spelling
- Do not invent skills, qualifications, experience,
  achievements, or technologies
- Keep the original meaning

Resume Summary:

{text}

Return only the improved professional summary.
"""

    return generate_ai_response(prompt)


# =====================================================
# IMPROVE PROJECT DESCRIPTION
# =====================================================

def improve_project(text):

    prompt = f"""
You are an expert ATS resume writer.

Rewrite the following project description.

Requirements:
- Use strong action verbs
- Make it professional
- Make it ATS-friendly
- Clearly explain what was done
- Keep it concise
- Do not invent technologies or achievements
- Preserve the original meaning

Project Description:

{text}

Return 2 to 4 professional resume bullet points.
"""

    return generate_ai_response(prompt)


# =====================================================
# IMPROVE WORK EXPERIENCE
# =====================================================

def improve_experience(text):

    prompt = f"""
You are an expert resume writer.

Rewrite the following work experience.

Requirements:
- Use strong action verbs
- Make it professional
- Make it ATS-friendly
- Clearly describe responsibilities
- Highlight achievements only when provided
- Correct grammar
- Do not invent information

Work Experience:

{text}

Return professional resume bullet points.
"""

    return generate_ai_response(prompt)


# =====================================================
# GENERATE ATS-FRIENDLY BULLET POINTS
# =====================================================

def generate_bullets(text):

    prompt = f"""
You are an ATS resume expert.

Convert the following resume content into strong
professional resume bullet points.

Requirements:
- Start each bullet with a strong action verb
- Use concise professional language
- Make the content ATS-friendly
- Preserve the original meaning
- Do not invent information
- Do not add fake numbers or achievements

Resume Content:

{text}

Return 3 to 5 professional bullet points.
"""

    return generate_ai_response(prompt)

def recommend_skill_improvements(missing_skills, job_description):
    """
    Generate AI recommendations based on missing skills
    and the job description.
    """

    prompt = f"""
You are an expert career advisor and ATS resume specialist.

A candidate has applied for a job.

JOB DESCRIPTION:
{job_description}

MISSING SKILLS:
{", ".join(missing_skills)}

Provide useful recommendations for the candidate.

Requirements:
- Explain which missing skills are important for this job.
- Suggest what the candidate should learn first.
- Give practical learning suggestions.
- Suggest how the candidate can improve their resume.
- Do not invent experience or qualifications.
- Keep the response concise and professional.

Return the recommendations in clear bullet points.
"""

    return generate_ai_response(prompt)

def analyze_resume_for_job(resume_text, job_description, missing_skills):
    """
    Analyze a resume against a job description and provide
    AI-powered improvement suggestions.
    """

    prompt = f"""
You are an expert ATS resume consultant.

Analyze the candidate's resume against the job description.

RESUME:
{resume_text}

JOB DESCRIPTION:
{job_description}

MISSING SKILLS:
{", ".join(missing_skills)}

Provide practical resume improvement suggestions.

Focus on:
- Missing keywords
- Skills that should be highlighted
- Sections that could be improved
- ATS optimization
- Professional wording
- How to better match the job description

Important:
- Do not invent experience.
- Do not invent skills.
- Do not create fake achievements.
- Only recommend changes supported by the candidate's information.

Return the response using clear headings and bullet points.
"""

    return generate_ai_response(prompt)