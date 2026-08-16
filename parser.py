import re
import pandas as pd


# -------------------------------
# Extract Name
# -------------------------------
def extract_name(text):

    lines = text.split("\n")

    for line in lines:

        line = line.strip()

        if len(line.split()) >= 2 and len(line.split()) <= 4:
            return line

    return "Not Found"


# -------------------------------
# Extract Email
# -------------------------------
def extract_email(text):

    email = re.findall(
        r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}",
        text
    )

    if email:
        return email[0]

    return "Not Found"


# -------------------------------
# Extract Phone
# -------------------------------
def extract_phone(text):

    phone = re.findall(
        r"(?:\+91[- ]?)?[6-9]\d{9}",
        text
    )

    if phone:
        return phone[0]

    return "Not Found"


# -------------------------------
# Extract LinkedIn
# -------------------------------
def extract_linkedin(text):

    linkedin = re.findall(
        r"(https?://(?:www\.)?linkedin\.com/in/[A-Za-z0-9_-]+|linkedin\.com/in/[A-Za-z0-9_-]+)",
        text
    )

    if linkedin:
        return linkedin[0]

    return "Not Found"


# -------------------------------
# Extract GitHub
# -------------------------------
def extract_github(text):

    github = re.findall(
        r"(https?://(?:www\.)?github\.com/[A-Za-z0-9_-]+|github\.com/[A-Za-z0-9_-]+)",
        text
    )

    if github:
        return github[0]

    return "Not Found"


# -------------------------------
# Extract Skills
# -------------------------------
def extract_skills(text):

    text = text.lower()

    skills_df = pd.read_csv("skills.csv")

    skills = skills_df["Skill"].dropna().tolist()

    found = []

    for skill in skills:

        if skill.lower() in text:
            found.append(skill)

    return sorted(list(set(found)))


# -------------------------------
# Extract Education
# -------------------------------
def extract_education(text):

    education_keywords = [

        "B.E",
        "B.Tech",
        "BCA",
        "B.Com",
        "B.Sc",
        "MBA",
        "MCA",
        "M.Tech",
        "M.Com",
        "Diploma",
        "Bachelor",
        "Master"

    ]

    text = text.lower()

    found = []

    for edu in education_keywords:

        if edu.lower() in text:
            found.append(edu)

    if found:
        return sorted(list(set(found)))

    return ["Not Found"]


# -------------------------------
# Extract Certifications
# -------------------------------
def extract_certifications(text):

    certification_keywords = [

        "Azure",
        "AWS",
        "Google Data Analytics",
        "Microsoft",
        "PL-300",
        "Oracle",
        "Cisco",
        "HackerRank",
        "Coursera",
        "Infosys",
        "NPTEL",
        "Simplilearn",
        "Udemy"

    ]

    text = text.lower()

    found = []

    for cert in certification_keywords:

        if cert.lower() in text:
            found.append(cert)

    if found:
        return sorted(list(set(found)))

    return ["Not Found"]