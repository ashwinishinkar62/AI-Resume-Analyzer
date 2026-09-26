from django.urls import path
from .import views

urlpatterns = [
    path('',views.home,name='home'),
    path('about/',views.about,name='about'),
    path('contact/',views.contact,name='contact'),
    path("upload/",views.upload_resume,name="upload_resume"),
    path("register/",views.register,name="register"),
    path("login/",views.user_login,name="login"),
    path("logout/",views.user_logout,name="logout"),
    path("history/",views.resume_history,name="resume_history"),
    path("delete/<int:resume_id>/",views.delete_resume,name="delete_resume"),
    path("analysis/<int:resume_id>/",views.resume_analysis,name="resume_analysis"),
    path("interview/<int:resume_id>/",views.interview_questions_view,name="interview_questions"),
    path("content/<int:resume_id>/",views.content_page,name="content_page"),
    path("download/<int:resume_id>/",views.download_pdf,name="download_pdf"),
    path("learning_roadmap/<int:resume_id>/",views.learning_roadmap,name="learning_roadmap"),
    path("learning_roadmap/",views.learning_roadmap_start,name="learning_roadmap_start"),
    path("roadmap/download/",views.download_roadmap_pdf,name="download_roadmap_pdf"),
    path("view-resume/<int:resume_id>/",views.view_resume,name="view_resume"),
]