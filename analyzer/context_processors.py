from .models import Resume

def latest_resume(request):
    if request.user.is_authenticated:
        resume = (Resume.objects.filter(user=request.user).order_by("-uploaded_at").first())
    else:
        resume = None
    return{"latest_resume":resume}