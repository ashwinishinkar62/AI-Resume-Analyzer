def generate_suggestions(text, skills, experience):
    suggestions = []
    text = text.lower()

    if "project" not in text:
        suggestions.append("Add your Projects.")

    if "certification" not in text:
        suggestions.append("Add your Certifications.")

    if "github.com" not in text:
        suggestions.append("Add Github Profile link.")

    if "linkedin.com" not in text:
        suggestions.append("Add LinkedIn Profile link.")

    if len(skills) < 5:
        suggestions.append("Add more relevant Technical Skills.")

    if experience == "Fresher":
        suggestions.append("Add Internship or Freelance Experience if available.")

    return suggestions