import re

def extract_projects(text):

    lines = [
        line.strip()
        for line in text.splitlines()
        if line.strip()
    ]

    projects = []
    project_section = False

    for line in lines:

        lower_line = line.lower().strip()

        # Start Projects section
        if lower_line in ["projects", "project", "technical projects"]:
            project_section = True
            continue

        # Stop at Education section
        if project_section and lower_line in [
            "education",
            "certifications & experience",
            "certifications",
            "experience",
            "career interests",
            "skills",
            "technical skills"
        ]:
            break

        if project_section:

            # Project description bullets are ignored
            if line.startswith(("•", "-", "●", "*")):
                continue

            # Ignore project status line
            if lower_line.startswith("project status"):
                continue

            # A project title contains "|"
            # because technologies are written after |
            if "|" in line:
                projects.append(line.strip())

    return projects