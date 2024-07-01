from django import forms
from app.models import PDFDocument

class uploadForm(forms.ModelForm):
    class Meta:
        model = PDFDocument
        fields = ['file']