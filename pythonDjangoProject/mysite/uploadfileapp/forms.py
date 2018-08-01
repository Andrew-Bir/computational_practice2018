# In forms.py...
from django import forms
from .models import UploadModel

class UploadForm(forms.ModelForm):
    class Meta:
        model = UploadModel
        fields = ["title", "file"]

class DetectForm(forms.Form):
    path = forms.CharField()
