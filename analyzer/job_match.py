from .skills import extract_skills

def calculate_job_match(resume_text,job_description):
    resume_skills = extract_skills(resume_text)
    job_skills = extract_skills(job_description)

    matched = list(set(resume_skills)& set(job_skills))
    missing = list(set(job_skills)- set(resume_skills))

    if len(job_skills) == 0:
        score = 0
    else:
        score = int((len(matched)/len(job_skills))* 100)

    return score, matched, missing