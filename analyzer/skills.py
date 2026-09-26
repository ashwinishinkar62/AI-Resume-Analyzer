import spacy
import re

nlp = spacy.load("en_core_web_sm")

KNOWN_SKILLS = [
    "Python",
    "Java",
    "C",
    "C++",
    "Django",
    "Flask",
    "HTML",
    "CSS",
    "JavaScript",
    "React",
    "Node.js",
    "SQL",
    "PostgreSQL",
    "MySQL",
    "SQLite",
    "Git",
    "GitHub",
    "Machine Learning",
    "Deep Learning",
    "TensorFlow",
    "PyTorch",
    "OpenCV",
    "NLP",
    "Generative AI",
    "Bootstrap",
    "Excel",
    "Power BI",
    "Pandas",
    "NumPy",
    "FastAPI",
    "REST API",
    "Docker",
    "Linux",
    "AWS"
]

def extract_skills(text):
    found_skills = []

    text_lower = text.lower()

    for skill in KNOWN_SKILLS:
        skill_lower = skill.lower()
        pattern = r"(?<!w)" + re.escape(skill_lower) + r"(?!\w)"

        if re.search(pattern, text_lower):
            found_skills.append(skill)
    return list(set(found_skills))