from django.contrib import admin
from .models import(Resume, ContactMessage)

admin.site.register(Resume)
@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ("name","email","created_at")
    search_fields = ("name","email","message")
    ordering = ("-created_at",)