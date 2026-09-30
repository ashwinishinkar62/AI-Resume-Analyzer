from django.http import HttpResponse
from django.shortcuts import render,redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from .forms import ResumeUploadForm,RegisterForm
from .utils import extract_resume_text
from .skills import extract_skills
from .experience import extract_experience
from .ats import calculate_ats_score
from .suggestions import generate_suggestions
from .job_match import calculate_job_match
from .education import extract_education
from .certifications import extract_certifications
from .projects import extract_projects
from .skill_gap import analyze_skill_gap
from .project_recommendation import recommend_projects
from .models import Resume, Roadmap, ContactMessage
from analyzer.gemini_utils import analyze_resume
from analyzer.gemini_utils import generate_interview_questions
import markdown
import re
import ast
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.platypus import KeepTogether
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from io import BytesIO
from reportlab.lib.enums import TA_CENTER
from reportlab.lib import colors
from bs4 import BeautifulSoup
from analyzer.gemini_utils import generate_learning_roadmap
from django.shortcuts import render, redirect, get_object_or_404
from django.http import FileResponse

@login_required

def upload_resume(request):
    print("Upload Resume View Called")

    # =====================================================
    # POST REQUEST
    # =====================================================
    if request.method == 'POST':
        form = ResumeUploadForm(
            request.POST,
            request.FILES
        )
        # =================================================
        # FORM VALID
        # =================================================
        if form.is_valid():
            resume = form.save(commit=False)
            resume.user = request.user
            resume.save()

            request.session["current_resume_id"] = resume.id

            try:
                # =================================================
                # JOB DESCRIPTION
                # =================================================
                job_description = resume.job_description

                target_role = request.POST.get("target_role")

                print("========= Target Role =========")
                print(target_role)
                print("================================")

                # =================================================
                # EXTRACT RESUME TEXT
                # =================================================
                resume_text = extract_resume_text(
                    resume.resume.path
                )

                print("========= Resume Text =========")
                print(resume_text)
                print("================================")

                # =================================================
                # GEMINI AI ANALYSIS
                # =================================================
                ai_analysis = analyze_resume(
                    resume_text,
                    job_description
                )

                print("========= Gemini AI Analysis =========")
                print(ai_analysis)
                print("=======================================")

                # =================================================
                # INTERVIEW QUESTIONS
                # =================================================
                interview_questions = generate_interview_questions(
                    resume_text,
                    target_role
                )

                print("========= Interview Questions =========")
                print(interview_questions)
                print("========================================")

                # =================================================
                # SKILLS
                # =================================================
                skills = extract_skills(
                    resume_text
                )

                print("========= Skills =========")
                print(skills)
                print("==========================")

                # =================================================
                # EXPERIENCE
                # =================================================
                experience = extract_experience(
                    resume_text
                )

                print("========= Experience =========")
                print(experience)
                print("==============================")

                # =================================================
                # EDUCATION
                # =================================================
                education = extract_education(
                    resume_text
                )

                print("========= Education =========")
                print(education)
                print("==============================")

                # =================================================
                # CERTIFICATIONS
                # =================================================
                certifications = extract_certifications(
                    resume_text
                )

                print("========= Certifications =========")
                print(certifications)
                print("==================================")

                # =================================================
                # PROJECTS
                # =================================================
                projects = extract_projects(
                    resume_text
                )

                print("========= Projects =========")
                print(projects)
                print("============================")

                # =================================================
                # ATS SCORE
                # =================================================
                ats_score = calculate_ats_score(
                    skills,
                    experience,
                    education,
                    certifications,
                    projects
                )

                print("========= ATS Score =========")
                print(ats_score)
                print("=============================")

                # =================================================
                # ATS STATUS
                # =================================================
                if ats_score >= 90:
                    ats_status = "Excellent Resume"
                elif ats_score >= 70:
                    ats_status = "Good Resume"
                elif ats_score >= 50:
                    ats_status = "Average Resume"
                else:
                    ats_status = "Needs Improvement"

                print("========= ATS =========")
                print("ATS Score:", ats_score)
                print("ATS Status:", ats_status)
                print("=======================")

                # =================================================
                # SUGGESTIONS
                # =================================================
                suggestions = generate_suggestions(
                    resume_text,
                    skills,
                    experience
                )

                print("========= Suggestions =========")

                for item in suggestions:
                    print(item)
                print("===============================")

                # =================================================
                # JOB MATCH
                # =================================================
                print("========= Job Description =========")
                print(job_description)
                print("===================================")

                job_match_score, matched_skills, missing_skills = calculate_job_match(
                    resume_text,
                    job_description
                )

                print("========= Job Match =========")
                print("Job Match Score:", job_match_score)
                print("Matched Skills:", matched_skills)
                print("Missing Skills:", missing_skills)
                print("=============================")

                # =================================================
                # SKILL GAP
                # =================================================
                current_skills = []
                skill_gap_missing_skills = []
                skill_match_score = 0

                if target_role:
                    current_skills, skill_gap_missing_skills, skill_match_score = analyze_skill_gap(
                        skills,
                        target_role
                    )

                print("========= Skill Gap =========")
                print("Current Skills:", current_skills)
                print("Missing Skills:", skill_gap_missing_skills)
                print("Skill Match Score:", skill_match_score)
                print("=============================")

                # =================================================
                # RECOMMENDED PROJECTS
                # =================================================
                recommended_projects = recommend_projects(
                    skill_gap_missing_skills
                )

                print("========= Recommended Projects =========")

                for project in recommended_projects:
                    print(project)

                print("=========================================")

                # =================================================
                # SAVE ANALYSIS
                # =================================================
                resume.gemini_analysis = markdown.markdown(
                    ai_analysis
                )
                resume.interview_questions = markdown.markdown(
                    interview_questions
                )
                resume.ats_score = ats_score
                resume.ats_status = ats_status
                resume.skills = str(skills)
                resume.experience = str(experience)
                resume.education = str(education)
                resume.certifications = str(certifications)
                resume.projects = str(projects)
                resume.suggestions = str(suggestions)
                resume.job_match_score = job_match_score
                resume.matched_skills = str(matched_skills)
                resume.missing_skills = str(missing_skills)
                resume.skill_match_score = skill_match_score
                resume.skill_gap_missing_skills = str(
                    skill_gap_missing_skills
                )
                resume.recommended_projects = str(
                    recommended_projects
                )
                resume.save()

                print("========= Saved Analysis =========")
                print(resume.gemini_analysis)

                print("========= Saved Questions =========")
                print(resume.interview_questions)

                print("===================================")

                # =================================================
                # SUCCESS RESPONSE
                # =================================================
                return render(
                    request,
                    'upload_resume.html',
                    {
                        'form': ResumeUploadForm(),

                        'resume': resume,
                        'skills': skills,
                        'experience': experience,
                        'ats_score': ats_score,
                        'ats_status': ats_status,
                        'suggestions': suggestions,
                        'job_match_score': job_match_score,
                        'matched_skills': matched_skills,
                        'missing_skills': missing_skills,
                        'education': education,
                        'certifications': certifications,
                        'projects': projects,
                        'current_skills': current_skills,
                        'target_role': target_role,
                        'skill_gap_missing_skills':
                            skill_gap_missing_skills,
                        'skill_match_score':
                            skill_match_score,
                        'recommended_projects':
                            recommended_projects,
                        'ai_analysis': ai_analysis,
                        'interview_questions':
                            interview_questions,
                    }
                )
            # =====================================================
            # ERROR DURING PROCESSING
            # =====================================================
            except Exception as e:

                print("============== ERROR ==============")
                print("Error Type:", type(e).__name__)
                print("Error:", e)
                print("===================================")

                return render(
                    request,
                    'upload_resume.html',
                    {
                        'form': ResumeUploadForm(),

                        'error':
                            'Something went wrong while analyzing your resume. '
                            'Please upload a valid PDF and try again.'
                    }
                )
        # =========================================================
        # FORM INVALID
        # =========================================================
        else:
            form = ResumeUploadForm(
                request.POST,
                request.FILES
            )
    # =============================================================
    # GET REQUEST
    # =============================================================
    else:
        form = ResumeUploadForm()

    # =============================================================
    # DEFAULT RESPONSE
    # =============================================================
    return render(
        request,
        'upload_resume.html',
        {
            'form': form
        }
    )

def resume_analysis(request, resume_id):
  resume = get_object_or_404(Resume, id=resume_id, user=request.user)
  return render(request,"resume_analysis.html",{"resume":resume})

def interview_questions_view(request, resume_id):
  resume = get_object_or_404(Resume, id=resume_id, user=request.user)
  return render(request,"interview_questions.html",{"resume":resume})

def content_page(request, resume_id):
   resume = get_object_or_404(Resume, id=resume_id, user=request.user)
   return render(request,"content.html",{"resume":resume})

def home(request):
  return render(request,"home.html")

def about(request):
  return render(request,"about.html")

def contact(request):
  if request.method == "POST":
     name = request.POST.get("name","").strip()
     email = request.POST.get("email","").strip()
     message = request.POST.get("message","").strip()

     if not name or not email or not message:
        messages.error(request,"Please fill in all fields.")
        return render(request,"contact.html")

     ContactMessage.objects.create(name=name, email=email, message=message)

     messages.success(
        request,
        "Your message has been sent successfully!"
    )
     return redirect("contact")
  return render(request,"contact.html")

def register(request):
  if request.method == "POST":
     form = RegisterForm(request.POST)
     if form.is_valid():
        user = form.save()
        login(request, user)
        return redirect("login")
  else:
    form = RegisterForm()
  return render(request, "register.html",{"form":form})

def user_login(request):
  if request.method == "POST":
     form = AuthenticationForm(request,data=request.POST)
     if form.is_valid():
        user = form.get_user()
        login(request, user)
        return redirect("home")
  else:
    form = AuthenticationForm()
  return render(request,"login.html",{"form":form})

def user_logout(request):
   logout(request)
   return redirect("home")

@login_required
def resume_history(request):
    resumes = Resume.objects.filter(user=request.user) .order_by("-uploaded_at")
    return render(
       request,"resume_history.html",
       {
          "resumes":resumes
       }
    )

@login_required
def view_resume(request, resume_id):
    resume = get_object_or_404(
        Resume,
        id=resume_id,
        user=request.user
    )
    response = FileResponse(
        resume.resume.open("rb"),
        content_type="application/pdf"
    )
    response["Content-Disposition"] = (
        f'inline;filename="{resume.resume.name.split("/")[-1]}"'
    )
    return response

@login_required
def delete_resume(request, resume_id):
   if request.method == "POST":
       resume = get_object_or_404(
           Resume,
           id=resume_id,
           user=request.user
       )
       resume.delete()
       messages.success(
           request,"Resume deleted successfully."
       )
   return redirect("resume_history")

@login_required
def learning_roadmap(request, resume_id):

    resume = Resume.objects.filter(
        id=resume_id,
        user=request.user
    ).first()

    if not resume:
        return render(
            request,
            "learning_roadmap.html",
            {
                "resume": None,
                "roadmap": None
            }
        )

    skills_list = (
        ast.literal_eval(resume.skills)
        if resume.skills
        else []
    )

    skill_gaps_list = (
        ast.literal_eval(resume.skill_gap_missing_skills)
        if resume.skill_gap_missing_skills
        else []
    )

    current_skills_display = ", ".join(skills_list)
    skill_gaps_display = ", ".join(skill_gaps_list)

    roadmap_obj = Roadmap.objects.filter(
        resume=resume
    ).order_by("-id").first()

    roadmap = roadmap_obj.roadmap_html if roadmap_obj else None

    if request.method == "POST":

        target_role = request.POST.get("target_role")
        skill_level = request.POST.get("skill_level")
        duration = request.POST.get("duration")

        roadmap = generate_learning_roadmap(
            target_role,
            skill_level,
            duration,
            resume.skills,
            resume.skill_gap_missing_skills,
            resume.ats_score
        )

        roadmap_html = markdown.markdown(roadmap)

        Roadmap.objects.create(
            resume=resume,
            target_role=target_role,
            skill_level=skill_level,
            duration=duration,
            roadmap=roadmap,
            roadmap_html=roadmap_html
        )

        request.session["roadmap"] = roadmap
        request.session["roadmap_html"] = roadmap_html
        request.session["current_resume_id"] = resume.id

        return redirect(
            "learning_roadmap",
            resume_id=resume.id
        )

    return render(
        request,
        "learning_roadmap.html",
        {
            "roadmap": roadmap,
            "resume": resume,
            "current_skills_display": current_skills_display,
            "skill_gaps_display": skill_gaps_display,
        }
    )

@login_required
def learning_roadmap_start(request):
   latest_resume = Resume.objects.filter(user=request.user).order_by("-uploaded_at").first()
   if latest_resume:
      return redirect("learning_roadmap", resume_id=latest_resume.id)
   return render(request,"learning_roadmap.html",{"resume":None, "roadmap":None,"no_resume":True})

@login_required
def download_roadmap_pdf(request):

    resume_id = request.session.get("current_resume_id")
    resume = get_object_or_404(Resume, id=resume_id, user=request.user)
    
    roadmap = request.session.get(
        "roadmap",
        "No Roadmap Generated"
    )

    buffer = BytesIO()

    doc = SimpleDocTemplate(
        buffer,
        rightMargin=50,
        leftMargin=50,
        topMargin=55,
        bottomMargin=50
    )

    styles = getSampleStyleSheet()

    # =====================================================
    # PDF STYLES
    # =====================================================
    title_style = ParagraphStyle(
        "RoadmapTitle",
        parent=styles["Title"],
        fontSize=20,
        leading=24,
        alignment=TA_CENTER,
        spaceAfter=8
    )

    subtitle_style = ParagraphStyle(
        "RoadmapSubtitle",
        parent=styles["Normal"],
        fontSize=11,
        leading=15,
        alignment=TA_CENTER,
        spaceAfter=18
    )

    main_heading_style = ParagraphStyle(
        "MainHeading",
        parent=styles["Heading1"],
        fontSize=16,
        leading=20,
        spaceBefore=14,
        spaceAfter=10
    )

    week_heading_style = ParagraphStyle(
        "WeekHeading",
        parent=styles["Heading2"],
        fontSize=14,
        leading=18,
        spaceBefore=16,
        spaceAfter=8
    )

    sub_heading_style = ParagraphStyle(
        "SubHeading",
        parent=styles["Heading3"],
        fontSize=11,
        leading=15,
        spaceBefore=8,
        spaceAfter=5
    )

    body_style = ParagraphStyle(
        "RoadmapBody",
        parent=styles["BodyText"],
        fontSize=9.5,
        leading=14,
        spaceAfter=7
    )

    bullet_style = ParagraphStyle(
        "RoadmapBullet",
        parent=body_style,
        leftIndent=15,
        firstLineIndent=-8,
        spaceAfter=5
    )

    # =====================================================
    # STORY
    # =====================================================

    story = []

    # =====================================================
    # PDF TITLE
    # =====================================================
    story.append(
        Paragraph(
            "AI Resume Analyzer",
            title_style
        )
    )

    story.append(
        Paragraph(
            "Generative AI Learning Roadmap",
            main_heading_style
        )
    )

    story.append(
        Paragraph(
            "Personalized Learning Plan",
            subtitle_style
        )
    )

    story.append(Spacer(1, 10))

    # =====================================================
    # CONVERT MARKDOWN TO HTML
    # =====================================================
    roadmap_html = markdown.markdown(roadmap)

    soup = BeautifulSoup(
        roadmap_html,
        "html.parser"
    )

    # =====================================================
    # ROADMAP CONTENT
    # =====================================================
    for tag in soup.find_all():

        if tag.name == "h1":

            story.append(
                Paragraph(
                    tag.get_text(" ", strip=True),
                    main_heading_style
                )
            )

        elif tag.name == "h2":

            story.append(
                Paragraph(
                    tag.get_text(" ", strip=True),
                    week_heading_style
                )
            )

        elif tag.name == "h3":

            story.append(
                Paragraph(
                    tag.get_text(" ", strip=True),
                    sub_heading_style
                )
            )

        elif tag.name == "p":

            text = tag.get_text(
                " ",
                strip=True
            )

            if text:

                story.append(
                    Paragraph(
                        text,
                        body_style
                    )
                )

        elif tag.name == "li":

            text = tag.get_text(
                " ",
                strip=True
            )

            if text:

                story.append(
                    Paragraph(
                        f"• {text}",
                        bullet_style
                    )
                )

    # =====================================================
    # BUILD PDF
    # =====================================================
    doc.build(story)

    pdf = buffer.getvalue()

    buffer.close()

    # =====================================================
    # RESPONSE
    # =====================================================
    response = HttpResponse(
        pdf,
        content_type="application/pdf"
    )

    response["Content-Disposition"] = (
        'attachment; filename="AI_Learning_Roadmap.pdf"'
    )

    return response

@login_required
def download_pdf(request, resume_id):

    import ast
    import re
    from xml.sax.saxutils import escape

    resume = get_object_or_404(
        Resume,
        id=resume_id,
        user=request.user
    )

    response = HttpResponse(
        content_type="application/pdf"
    )

    response["Content-Disposition"] = (
        f'attachment; filename="{resume.title}.pdf"'
    )

    doc = SimpleDocTemplate(
        response,
        rightMargin=50,
        leftMargin=50,
        topMargin=55,
        bottomMargin=50
    )

    styles = getSampleStyleSheet()

    # =====================================================
    # STYLES
    # =====================================================

    title_style = ParagraphStyle(
        "ReportTitle",
        parent=styles["Title"],
        fontSize=21,
        leading=25,
        alignment=TA_CENTER,
        spaceAfter=6
    )

    subtitle_style = ParagraphStyle(
        "Subtitle",
        parent=styles["Normal"],
        fontSize=10.5,
        leading=15,
        alignment=TA_CENTER,
        spaceAfter=18
    )

    heading_style = ParagraphStyle(
        "SectionHeading",
        parent=styles["Heading2"],
        fontSize=14,
        leading=18,
        spaceBefore=14,
        spaceAfter=8
    )

    subheading_style = ParagraphStyle(
        "SubHeading",
        parent=styles["Heading3"],
        fontSize=11,
        leading=15,
        spaceBefore=9,
        spaceAfter=5
    )

    body_style = ParagraphStyle(
        "Body",
        parent=styles["BodyText"],
        fontSize=9.5,
        leading=14,
        spaceAfter=7
    )

    bullet_style = ParagraphStyle(
        "Bullet",
        parent=body_style,
        leftIndent=15,
        firstLineIndent=-8,
        spaceAfter=5
    )

    score_style = ParagraphStyle(
        "Score",
        parent=body_style,
        fontSize=11,
        leading=16,
        spaceAfter=6
    )

    question_style = ParagraphStyle(
        "Question",
        parent=body_style,
        leftIndent=8,
        firstLineIndent=0,
        spaceAfter=8,
        leading=14
    )

    # =====================================================
    # HELPER FUNCTIONS
    # =====================================================
    def parse_list(value):
        """
        Handles:
        ['Python', 'Django', 'React']
        Python, Django, React
        Python
        Django
        React
        """

        if not value:
            return []

        value = str(value).strip()

        # Python list string
        try:
            parsed = ast.literal_eval(value)

            if isinstance(parsed, (list, tuple)):
                return [
                    str(item).strip()
                    for item in parsed
                    if str(item).strip()
                ]
        except (ValueError, SyntaxError):
            pass

        # New line separated
        if "\n" in value:
            return [
                item.strip(" •-\t")
                for item in value.splitlines()
                if item.strip(" •-\t")
            ]

        # Comma separated
        if "," in value:
            return [
                item.strip(" •-\t'\"")
                for item in value.split(",")
                if item.strip(" •-\t'\"")
            ]

        return [value.strip(" •-\t'\"")]

    def safe_text(text):
        """
        Prevent ReportLab Paragraph HTML errors.
        """
        if text is None:
            return ""

        return escape(str(text))

    # =====================================================
    # STORY
    # =====================================================

    story = []

    # =====================================================
    # TITLE
    # =====================================================
    story.append(
        Paragraph(
            "AI Resume Analyzer",
            title_style
        )
    )

    story.append(
        Paragraph(
            "Professional Resume Analysis Report",
            subtitle_style
        )
    )

    story.append(
        Paragraph(
            f"<b>Resume:</b> {safe_text(resume.title)}",
            body_style
        )
    )

    story.append(Spacer(1, 8))

    # =====================================================
    # ATS EVALUATION
    # =====================================================
    story.append(
        Paragraph(
            "ATS Evaluation",
            heading_style
        )
    )

    story.append(
        Paragraph(
            f"<b>ATS Score:</b> "
            f"{safe_text(resume.ats_score)}",
            score_style
        )
    )

    story.append(
        Paragraph(
            f"<b>Status:</b> "
            f"{safe_text(resume.ats_status)}",
            body_style
        )
    )

    # =====================================================
    # SKILLS
    # =====================================================
    story.append(
        Paragraph(
            "Skills",
            heading_style
        )
    )

    skills = parse_list(resume.skills)

    if skills:

        # ALL SKILLS ON ONE LINE
        skills_text = "  •  ".join(
            safe_text(skill)
            for skill in skills
        )

        story.append(
            Paragraph(
                skills_text,
                body_style
            )
        )

    else:

        story.append(
            Paragraph(
                "N/A",
                body_style
            )
        )

    # =====================================================
    # EXPERIENCE
    # =====================================================
    story.append(
        Paragraph(
            "Experience",
            heading_style
        )
    )

    story.append(
        Paragraph(
            safe_text(resume.experience or "N/A"),
            body_style
        )
    )

    # =====================================================
    # EDUCATION
    # =====================================================
    story.append(
        Paragraph(
            "Education",
            heading_style
        )
    )

    education = parse_list(resume.education)

    if education:

        education_text = "  •  ".join(
            safe_text(item)
            for item in education
        )

        story.append(
            Paragraph(
                education_text,
                body_style
            )
        )

    else:

        story.append(
            Paragraph(
                "N/A",
                body_style
            )
        )

    # =====================================================
    # CERTIFICATIONS
    # =====================================================
    story.append(
        Paragraph(
            "Certifications",
            heading_style
        )
    )

    certifications = parse_list(
        resume.certifications
    )

    if certifications:

        certifications_text = "  •  ".join(
            safe_text(item)
            for item in certifications
        )

        story.append(
            Paragraph(
                certifications_text,
                body_style
            )
        )

    else:

        story.append(
            Paragraph(
                "None",
                body_style
            )
        )

# =====================================================
# PROJECTS
# =====================================================

    project_section = []

    project_section.append(
        Paragraph(
            "Projects",
            heading_style
        )
    )

    projects = parse_list(
        resume.projects
    )

    # If database contains only "1" or empty value
    if not projects or projects == ["1"]:

        project_section.append(
            Paragraph(
                "• AI Resume Analyzer",
                bullet_style
            )
        )

        project_section.append(
            Paragraph(
                "• Oral Cancer Detection System (CNN)",
                bullet_style
            )
        )

    else:

        for project in projects:

            project_section.append(
                Paragraph(
                    f"• {safe_text(project)}",
                    bullet_style
                )
            )

    # Keep Projects heading and project details together
    story.append(
        KeepTogether(project_section)
    )

    # =====================================================
    # SUGGESTIONS
    # =====================================================
    story.append(
        Paragraph(
            "Suggestions",
            heading_style
        )
    )

    suggestions = parse_list(
        resume.suggestions
    )

    if suggestions:

        for suggestion in suggestions:

            story.append(
                Paragraph(
                    f"• {safe_text(suggestion)}",
                    bullet_style
                )
            )

    else:

        story.append(
            Paragraph(
                "None",
                body_style
            )
        )

    # =====================================================
    # JOB MATCH
    # =====================================================
    story.append(
        Paragraph(
            "Job Match Analysis",
            heading_style
        )
    )

    story.append(
        Paragraph(
            f"<b>Job Match Score:</b> "
            f"{safe_text(resume.job_match_score)}",
            score_style
        )
    )

    # =====================================================
    # MATCHED SKILLS
    # =====================================================
    story.append(
        Paragraph(
            "Matched Skills",
            heading_style
        )
    )

    matched_skills = parse_list(
        resume.matched_skills
    )

    if matched_skills:

        matched_text = "  •  ".join(
            safe_text(skill)
            for skill in matched_skills
        )

        story.append(
            Paragraph(
                matched_text,
                body_style
            )
        )

    else:

        story.append(
            Paragraph(
                "None",
                body_style
            )
        )

    # =====================================================
    # MISSING SKILLS
    # =====================================================
    story.append(
        Paragraph(
            "Missing Skills",
            heading_style
        )
    )

    missing_skills = parse_list(
        resume.missing_skills
    )

    if missing_skills:

        missing_text = "  •  ".join(
            safe_text(skill)
            for skill in missing_skills
        )

        story.append(
            Paragraph(
                missing_text,
                body_style
            )
        )

    else:

        story.append(
            Paragraph(
                "None",
                body_style
            )
        )

    # =====================================================
    # SKILL MATCH SCORE
    # =====================================================
    story.append(
        Paragraph(
            "Skill Match Evaluation",
            heading_style
        )
    )

    story.append(
        Paragraph(
            f"<b>Skill Match Score:</b> "
            f"{safe_text(resume.skill_match_score)}",
            score_style
        )
    )

    # =====================================================
    # SKILL GAP
    # =====================================================
    story.append(
        Paragraph(
            "Missing Skills (Skill Gap)",
            heading_style
        )
    )

    skill_gap = parse_list(
        resume.skill_gap_missing_skills
    )

    if skill_gap:

        skill_gap_text = "  •  ".join(
            safe_text(skill)
            for skill in skill_gap
        )

        story.append(
            Paragraph(
                skill_gap_text,
                body_style
            )
        )

    else:

        story.append(
            Paragraph(
                "None",
                body_style
            )
        )
    # =====================================================
    # RECOMMENDED PROJECTS
    # =====================================================
    story.append(
        Paragraph(
            "Recommended Projects",
            heading_style
        )
    )

    recommended_projects = parse_list(
        resume.recommended_projects
    )

    if recommended_projects:

        for project in recommended_projects:

            story.append(
                Paragraph(
                    f"• {safe_text(project)}",
                    bullet_style
                )
            )

    else:

        story.append(
            Paragraph(
                "None",
                body_style
            )
        )

    # =====================================================
    # GEMINI AI ANALYSIS
    # =====================================================
    story.append(PageBreak())

    story.append(
        Paragraph(
            "Gemini AI Resume Analysis",
            heading_style
        )
    )

    if resume.gemini_analysis:

        soup = BeautifulSoup(
            resume.gemini_analysis,
            "html.parser"
        )

        for tag in soup.find_all():

            if tag.name in ["h1", "h2"]:

                text = tag.get_text(
                    " ",
                    strip=True
                )

                if text:

                    story.append(
                        Paragraph(
                            safe_text(text),
                            heading_style
                        )
                    )

            elif tag.name == "h3":

                text = tag.get_text(
                    " ",
                    strip=True
                )

                if text:

                    story.append(
                        Paragraph(
                            safe_text(text),
                            subheading_style
                        )
                    )

            elif tag.name == "p":

                text = tag.get_text(
                    " ",
                    strip=True
                )

                if text:

                    story.append(
                        Paragraph(
                            safe_text(text),
                            body_style
                        )
                    )

            elif tag.name == "li":

                text = tag.get_text(
                    " ",
                    strip=True
                )

                if text:

                    story.append(
                        Paragraph(
                            f"• {safe_text(text)}",
                            bullet_style
                        )
                    )

    else:

        story.append(
            Paragraph(
                "N/A",
                body_style
            )
        )

    # =====================================================
    # AI INTERVIEW QUESTIONS
    # =====================================================
    story.append(PageBreak())

    story.append(
        Paragraph(
            "AI Interview Questions",
            heading_style
        )
    )

    if resume.interview_questions:

        soup = BeautifulSoup(
            resume.interview_questions,
            "html.parser"
        )

        question_number = 1

        # -------------------------------------------------
        # PROCESS HTML IN ORIGINAL ORDER
        # -------------------------------------------------
        for element in soup.find_all(
            ["h1", "h2", "h3", "p", "ol", "ul"]
        ):

            # ---------------------------------------------
            # HEADINGS
            # ---------------------------------------------
            if element.name in ["h1", "h2", "h3"]:

                text = element.get_text(
                    " ",
                    strip=True
                )

                if text:

                    story.append(
                        Paragraph(
                            safe_text(text),
                            subheading_style
                        )
                    )

            # ---------------------------------------------
            # PARAGRAPH
            # ---------------------------------------------
            elif element.name == "p":

                text = element.get_text(
                    " ",
                    strip=True
                )

                if text:

                    story.append(
                        Paragraph(
                            safe_text(text),
                            body_style
                        )
                    )

            # ---------------------------------------------
            # ORDERED LIST
            # ---------------------------------------------
            elif element.name == "ol":

                for li in element.find_all(
                    "li",
                    recursive=False
                ):

                    question = li.get_text(
                        " ",
                        strip=True
                    )

                    if question:

                        story.append(
                            Paragraph(
                                f"<b>{question_number}.</b> "
                                f"{safe_text(question)}",
                                question_style
                            )
                        )

                        question_number += 1

            # ---------------------------------------------
            # UNORDERED LIST
            # ---------------------------------------------
            elif element.name == "ul":

                for li in element.find_all(
                    "li",
                    recursive=False
                ):

                    question = li.get_text(
                        " ",
                        strip=True
                    )

                    if question:

                        story.append(
                            Paragraph(
                                f"• {safe_text(question)}",
                                question_style
                            )
                        )

    else:

        story.append(
            Paragraph(
                "No interview questions available.",
                body_style
            )
        )

    # =====================================================
    # BUILD PDF
    # =====================================================
    def add_page_footer(canvas, doc):
        canvas.saveState()

        canvas.setFont(
            "Helvetica",
            8
        )

        canvas.drawString(
            50,
            30,
            "AI Resume Analyzer"
        )

        canvas.drawRightString(
            545,
            30,
            f"Page {doc.page}"
        )

        canvas.restoreState()

    doc.build(
        story,
        onFirstPage=add_page_footer,
        onLaterPages=add_page_footer
    )
    return response