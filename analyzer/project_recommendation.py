def recommend_projects(missing_skills):
    recommendations = []

    if "REST API" in missing_skills:
        recommendations.append("Build a Django REST API Project")
    if "Docker" in missing_skills:
        recommendations.append("Dockerize your Django Project")
    if "React" in missing_skills:
        recommendations.append("Build a React Portfolio Website")
    if "Git" in missing_skills:
        recommendations.append("Upload all projects to GitHub")
    if "PostgreSQL" in missing_skills:
        recommendations.append("Build a PostgreSQL CRUD Application")
    if "Power BI" in missing_skills:
        recommendations.append("Create a Sales Dashboard in Power BI")
    if "Excel" in missing_skills:
        recommendations.append("Build a Excel Data Analysis Project")
    if len(recommendations) == 0:
        recommendations.append("Excellent! Your skills match the selected role.")
    return recommendations