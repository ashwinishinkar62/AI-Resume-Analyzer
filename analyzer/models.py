from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

class Resume(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="resumes")
    title = models.CharField(max_length=100)
    resume = models.FileField(upload_to='resume/')
    job_description = models.TextField(blank=True, null=True)
    gemini_analysis = models.TextField(blank=True, null=True)
    interview_questions = models.TextField(blank=True, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    ats_score = models.IntegerField(default=0, validators=[MinValueValidator(0),MaxValueValidator(100)])
    ats_status = models.CharField(max_length=100,blank=True)
    skills =  models.TextField(blank=True)
    experience = models.TextField(blank=True)
    education = models.TextField(blank=True)
    certifications = models.TextField(blank=True)
    projects = models.TextField(blank=True)
    suggestions = models.TextField(blank=True)
    job_match_score = models.IntegerField(default=0, validators=[MinValueValidator(0),MaxValueValidator(100)])
    matched_skills = models.TextField(blank=True)
    missing_skills = models.TextField(blank=True)
    skill_match_score = models.IntegerField(default=0, validators=[MinValueValidator(0),MaxValueValidator(100)])
    skill_gap_missing_skills = models.TextField(blank=True)
    recommended_projects = models.TextField(blank=True)

    def __str__(self):
      return self.title

class Roadmap(models.Model):
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE, related_name="roadmap")
    target_role = models.CharField(max_length=100)
    skill_level = models.CharField(max_length=100)
    duration = models.CharField(max_length=50)

    roadmap = models.TextField()
    roadmap_html = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
      return f"{self.target_role} - {self.duration}"

class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
       return self.name