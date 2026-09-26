def calculate_ats_score(
    skills,
    experience,
    education,
    certifications,
    projects
):
    score = 0

    # Skills (Max 40)
    score += min(len(skills) * 4, 40)

    # Experience (20)
    if experience != "Fresher":
        score += 20

    # Education (10)
    if education != ["Not Found"]:
        score += 10

    # Certifications (10)
    if certifications != ["Not Found"]:
        score += 10

    # Projects (20)
    if projects:
        score += 20

    return min(score, 100)