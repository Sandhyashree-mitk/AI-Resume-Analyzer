# -------------------------------
# ATS Score Calculator
# -------------------------------

def calculate_ats_score(
    name,
    email,
    phone,
    linkedin,
    github,
    skills,
    education,
    certifications,
    text
):

    score = 0

    # Basic Information
    if name != "Not Found":
        score += 10

    if email != "Not Found":
        score += 10

    if phone != "Not Found":
        score += 10

    if linkedin != "Not Found":
        score += 10

    if github != "Not Found":
        score += 10

    # Skills
    if len(skills) >= 8:
        score += 20
    elif len(skills) >= 5:
        score += 15
    elif len(skills) >= 3:
        score += 10

    # Education
    if "Not Found" not in education:
        score += 10

    # Certifications
    if "Not Found" not in certifications:
        score += 10

    # Resume Length
    words = len(text.split())

    if words >= 300:
        score += 10
    elif words >= 200:
        score += 5

    return min(score, 100)


# -------------------------------
# Resume Suggestions
# -------------------------------

def get_resume_suggestions(
    email,
    phone,
    linkedin,
    github,
    skills,
    education,
    certifications,
    text
):

    suggestions = []

    if email == "Not Found":
        suggestions.append("📧 Add your Email Address.")

    if phone == "Not Found":
        suggestions.append("📱 Add your Phone Number.")

    if linkedin == "Not Found":
        suggestions.append("🔗 Add your LinkedIn Profile.")

    if github == "Not Found":
        suggestions.append("💻 Add your GitHub Profile.")

    if len(skills) < 5:
        suggestions.append("🛠 Add more relevant technical skills.")

    if "Not Found" in education:
        suggestions.append("🎓 Mention your Education details.")

    if "Not Found" in certifications:
        suggestions.append("📜 Add Certifications to strengthen your resume.")

    if len(text.split()) < 250:
        suggestions.append("📝 Expand your resume with projects, achievements, and experience.")

    if not suggestions:
        suggestions.append("🎉 Excellent! Your resume looks ATS-friendly.")

    return suggestions