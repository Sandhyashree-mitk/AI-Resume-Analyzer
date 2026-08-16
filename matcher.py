# ---------------------------------------
# Job Description Matching
# ---------------------------------------

def match_resume(skills, job_description):

    # If no job description is entered
    if not job_description.strip():
        return 0, [], []

    # Convert job description to lowercase
    job_text = job_description.lower()

    matched = []
    missing = []

    # Compare each resume skill with job description
    for skill in skills:

        if skill.lower() in job_text:
            matched.append(skill)
        else:
            missing.append(skill)

    # Calculate Match Percentage
    if len(skills) == 0:
        score = 0
    else:
        score = round((len(matched) / len(skills)) * 100)

    return score, matched, missing