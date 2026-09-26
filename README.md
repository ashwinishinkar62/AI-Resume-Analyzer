AI Resume Analyzer

An AI-powered web application that analyzes resumes, evaluates ATS compatibility, identifies skill gaps, matches resumes with job descriptions, and provides AI-based career assistance.

🚀 Features

- 📄 Resume upload with PDF-only validation
- 🔐 User registration, login and logout
- 📊 ATS score and ATS status
- 🤖 AI-powered resume analysis using Google Gemini
- 💼 Job description matching
- 🧠 Skill match and skill gap analysis
- 💡 Resume improvement suggestions
- 🎯 AI-generated interview questions
- 🗺️ Personalized AI learning roadmap
- 📑 Resume analysis PDF report
- 📥 Learning roadmap PDF download
- 📚 Resume history
- 👁️ Secure resume viewing
- 🗑️ Resume deletion
- 📱 Responsive design for desktop and mobile
- 📩 Contact form
- 🔒 User-specific resume access

🛠️ Technologies Used

Frontend

- HTML5
- CSS3
- Tailwind CSS
- JavaScript

Backend

- Python
- Django

AI

- Google Gemini API

Database

- SQLite

Libraries

- PyMuPDF
- python-docx
- Markdown
- ReportLab

Development Tools

- VS Code
- Git
- GitHub

⚙️ How It Works

1. User creates an account or logs in.
2. User uploads a resume in PDF format.
3. The application extracts text from the resume.
4. Resume data is analyzed for ATS compatibility.
5. The system identifies skills, experience, education, certifications and projects.
6. Users can provide a job description for job matching.
7. The application calculates job match, skill match and skill gaps.
8. Google Gemini generates:
   - Resume analysis
   - Interview questions
   - Personalized learning roadmap
9. Users can view their resume history and download generated reports.

📊 Resume Analysis

The application provides:

- ATS Score
- ATS Status
- Resume Summary
- Resume Strengths
- Resume Weaknesses
- Missing Skills
- Improvement Suggestions
- Career Advice

💼 Job & Skill Analysis

The application compares the uploaded resume with a job description and provides:

- Job Match Score
- Matched Skills
- Missing Skills
- Skill Match Score
- Skill Gap Analysis
- Recommended Projects

🤖 AI Career Assistance

Google Gemini is used to generate:

AI Resume Analysis

Analyzes the resume against the provided job description.

AI Interview Questions

Generates questions in different difficulty levels:

- Easy
- Medium
- Hard
- HR

AI Learning Roadmap

Generates a personalized roadmap based on:

- Target role
- Current skill level
- Duration
- Current skills
- Identified skill gaps
- ATS score

🔐 Security

The application includes:

- User authentication
- CSRF protection
- User-specific resume access
- Protected resume viewing
- Protected PDF downloads
- Protected resume deletion
- Environment variables for sensitive API keys
- PDF file type validation
- Maximum file size validation

📁 Project Structure

AI Resume Analyzer/
│
├── analyzer/
│   ├── migrations/
│   ├── templates/
│   ├── gemini_utils.py
│   ├── models.py
│   ├── views.py
│   ├── forms.py
│   └── ...
│
├── config/
│   ├── settings.py
│   ├── urls.py
│   └── ...
│
├── templates/
│
├── theme/
│
├── media/
│
├── manage.py
├── requirements.txt
├── .gitignore
├── .env.example
└── README.md

💻 Installation

1. Clone the repository

git clone YOUR_GITHUB_REPOSITORY_URL
cd "AI Resume Analyzer"

2. Create a virtual environment

python -m venv venv

3. Activate the virtual environment

Windows

venv\Scripts\activate

4. Install dependencies

pip install -r requirements.txt

5. Create environment variables

Create a ".env" file in the project root:

GEMINI_API_KEY=your_actual_api_key
DEBUG=True

Never upload the actual ".env" file or API key to GitHub.

6. Apply migrations

python manage.py migrate

7. Run the development server

python manage.py runserver

Open:

http://127.0.0.1:8000/

🔑 Environment Variables

Variable| Description
"GEMINI_API_KEY"| Google Gemini API key
"DEBUG"| Django debug setting

Use ".env.example" as a reference for configuring the project.

📌 Future Improvements

Possible future improvements include:

- Migration to the latest Google Gemini Python SDK
- Deployment to a cloud platform
- Additional resume formats
- More advanced ATS analysis
- Additional job-role templates

👩‍💻 Author

Ashwini Shinkar

B.Tech Computer Engineering

📄 License

This project was developed as a portfolio/final-year project for learning and demonstration purposes.