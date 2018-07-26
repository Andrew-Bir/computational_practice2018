from django import forms
from .models import TestModel

class TestForm(forms.ModelForm):
    class Meta:
        model = TestModel
        fields = ["file"]

class IdentifyForm(forms.Form):
    path = forms.CharField()
