import google.generativeai as genai
from django.conf import settings

genai.configure(api_key=settings.GEMINI_API_KEY)

#print("API KEY:",settings.GEMINI_API_KEY)
#for m in genai.list_models():
    #print(m.name)

model = genai.GenerativeModel("gemini-3.5-flash")

def analyze_resume(resume_text, job_description):

    prompt = f"""
You are an ATS Resume Analyzer.

Analyze the following resume against the given job description.

Resume:
{resume_text}

Job Description:
{job_description}

IMPORTANT:
Return ONLY Markdown.
Do not return HTML.
Do not add any introduction or conclusion.

Use EXACTLY these headings:

## Resume Summary
Write a short summary in 2-3 sentences.

## Resume Strengths
- Point 1
- Point 2
- Point 3

## Resume Weaknesses
- Point 1
- Point 2

## Missing Skills
- Point 1
- Point 2

## Improvement Suggestions
- Point 1
- Point 2
- Point 3

## Career Advice
- Point 1
- Point 2

STRICT FORMATTING RULES:
1. Every heading MUST start with ## followed by a space.
2. Every bullet point MUST start with "- " (hyphen followed by one space).
3. Do not write headings as normal paragraphs.
4. Do not remove or rename any heading.
5. Do not use numbered lists.
6. Keep the response clean and professional.
"""

    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        print("Gemini Error:", e)
        return f"Gemini Error: {e}"

    
def generate_interview_questions(resume_text, target_role):

    prompt = f"""
You are an expert technical interviewer.

Resume:
{resume_text}

Target Role:
{target_role}

Generate interview questions relevant to the resume and target role.

Return ONLY Markdown.

Use EXACTLY this structure:

## Easy Questions

1. Question
2. Question
3. Question
4. Question
5. Question

## Medium Questions

1. Question
2. Question
3. Question
4. Question
5. Question

## Hard Questions

1. Question
2. Question
3. Question
4. Question
5. Question

## HR Questions

1. Question
2. Question
3. Question
4. Question
5. Question

STRICT FORMATTING RULES:
1. Every section heading MUST start with ## followed by a space.
2. Every question MUST be on a separate line.
3. Every question MUST start with its number followed by a period and a space.
4. Use exactly 5 questions in each section.
5. Do not use bullet points.
6. Do not add answers.
7. Do not add explanations.
8. Do not add any introduction or conclusion.
9. Keep questions relevant to the target role and uploaded resume.
"""

    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        print("Gemini Error:", e)
        return f"Gemini Error: {e}"


def generate_learning_roadmap(target_role, skill_level, duration, current_skills, missing_skills, ats_score):
    prompt = f"""
You are an expect career mentor and AI learning roadmap generator.

Create a PERSONALIZED AI Learning Roadmap based on the user's uploaded resume analysis.

IMPORTANT:
The Roadmap MUST be based on the user's current skills and identified skill gaps.

Target Role:
{target_role}

Current Skill Level:
{skill_level}

Duration:
{duration}

Current Skills from Resume:
{current_skills}

Missing Skills/Skill Gaps from Resume Analysis:
{missing_skills}

ATS Score:
{ats_score}

Rules:
1. Do NOT recommend beginner topics that the user already knows unless they are required at an advanced level.
2. Give highest priority to the identified missing skills.
3. Connect the learning plan to the target role.
4. Make the roadmap practical and achievable within the selected duration.
5. Include weekly learning goals.
6. Include practical projects wherever useful.
7. Include recommended resources/topics.
8. Include interview preparation.
9. Clearly mention that the roadmap is based on the uploaded resume.
10. Keeply the response clean and well formatted.

Format:

#Personalized AI Learning Roadmap 
## Resume Analysis Summary 
Target Role:
ATS Score:
Current Skills:
Skill Gaps:

## Week 1
Topics:
- ...

Practical Task:
-...

## Week 2
Topics:
- ...

Practical Task:
-...

Continue until the selected duration is completed.

## Recommended Projects
- ...

## Interview Preparation
- ...

## Final Recommendations
- ...

Do not provide generic advice unrelated to the user's resume.
"""

    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Gemini Error:{e}"