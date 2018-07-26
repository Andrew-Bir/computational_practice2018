from django.db import models

# Create your models here.
from django.forms import ModelForm

class TestModel(models.Model):
   file = models.FileField(upload_to="tests/%Y-%m-%d/%H-%M-%S/", blank=True)
