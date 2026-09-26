from django import forms
from .models import Resume
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

class ResumeUploadForm(forms.ModelForm):
    class Meta:
        model = Resume

        fields = [
            'title',
            'resume',
            'job_description'
        ]

        widgets = {

            'title': forms.TextInput(attrs={
                'class': 'w-full p-3 border border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500',
                'placeholder': 'Enter Resume Title'
            }),

            'resume': forms.ClearableFileInput(attrs={
                'class': 'w-full p-3 border border-gray-300 rounded-xl bg-white',
                'accept': '.pdf,application/pdf'
            }),

            'job_description': forms.Textarea(attrs={
                'class': 'w-full p-3 border border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500',
                'placeholder': 'Paste Job Description Here...',
                'rows': 8,
            })
        }

    def clean_resume(self):

        resume = self.cleaned_data.get('resume')

        if not resume:
            raise ValidationError(
                "Please upload your resume."
            )

        # Check file extension
        if not resume.name.lower().endswith('.pdf'):
            raise ValidationError(
                "Only PDF files are allowed."
            )

        # Check content type
        if resume.content_type != 'application/pdf':
            raise ValidationError(
                "Invalid file type. Please upload a valid PDF file."
            )

        # File size limit: 5 MB
        if resume.size > 5 * 1024 * 1024:
            raise ValidationError(
                "File size must be less than 5 MB."
            )

        return resume

class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["username","password1","password2"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            field.widget.attrs.update({
                "class":"w-full p-3 border border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500"
            })