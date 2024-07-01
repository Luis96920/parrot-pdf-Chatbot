from django.contrib import admin
from .models import PDFDocument
from .models import Profile
# Register your models here.
admin.site.register(Profile)
admin.site.register(PDFDocument)

