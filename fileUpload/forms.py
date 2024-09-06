from django import forms

from .models import Document

class UploadForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ('document',) # points to 'document' field in models.py


class EmailForm(forms.Form):
    name = forms.CharField(max_length=100)
    receiver_email = forms.EmailField()