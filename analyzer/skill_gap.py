ROLE_SKILLS = {
    "Backend Developer":[
        "Python",
        "Django",
        "SQL",
        "REST API",
        "Git",
        "Docker",
        "PostgreSQL"
    ],
    "Frontend Developer":[
        "HTML",
        "CSS",
        "JavaScript",
        "React",
        "Bootstrap",
        "Git"
    ],
    "Full Stack Developer":[
        "HTML",
        "CSS",
        "JavaScript",
        "React",
        "Python",
        "Django",
        "SQL",
        "Git"
    ],
    "Python Developer":[
        "Python",
        "Django",
        "Flask",
        "SQL",
        "Git"
    ],
    "Data Analyst":[
        "Python",
        "SQL",
        "Excel",
        "Power BI",
        "Pandas",
        "NumPy"
    ]
}
def analyze_skill_gap(user_skills, target_role):
 required_skills = ROLE_SKILLS.get(target_role, [])
 current_skills = []
 missing_skills = []

 for skill in required_skills:
   if skill in user_skills:
      current_skills.append(skill)
   else:
     missing_skills.append(skill)
 if len(required_skills) == 0:
    match_score = 0
 else:
   match_score = int((len(current_skills)/len(required_skills)) *100)
 return current_skills, missing_skills, match_score