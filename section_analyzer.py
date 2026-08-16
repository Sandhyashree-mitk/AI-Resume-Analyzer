import re

def analyze_sections(text):

    text = text.lower()

    sections = {}

    # Contact Information
    email = re.search(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}", text)
    phone = re.search(r"[6-9]\d{9}", text)

    if email and phone:
        sections["Contact"] = "✅ Complete"
    else:
        sections["Contact"] = "❌ Missing"

    # Skills
    if "skills" in text:
        sections["Skills"] = "✅ Present"
    else:
        sections["Skills"] = "❌ Missing"

    # Education
    education_keywords = [
        "b.e", "b.tech", "bca", "mca",
        "mba", "b.com", "m.tech",
        "degree", "university", "college"
    ]

    if any(word in text for word in education_keywords):
        sections["Education"] = "✅ Present"
    else:
        sections["Education"] = "❌ Missing"

    # Projects
    if "project" in text or "projects" in text:
        sections["Projects"] = "✅ Present"
    else:
        sections["Projects"] = "❌ Missing"

    # Experience
    experience_keywords = [
        "experience",
        "internship",
        "intern",
        "worked",
        "employment"
    ]

    if any(word in text for word in experience_keywords):
        sections["Experience"] = "✅ Present"
    else:
        sections["Experience"] = "❌ Missing"

    # Certifications
    certification_keywords = [
        "certificate",
        "certification",
        "azure",
        "aws",
        "coursera",
        "hackerrank",
        "nptel",
        "udemy"
    ]

    if any(word in text for word in certification_keywords):
        sections["Certifications"] = "✅ Present"
    else:
        sections["Certifications"] = "❌ Missing"

    return sections