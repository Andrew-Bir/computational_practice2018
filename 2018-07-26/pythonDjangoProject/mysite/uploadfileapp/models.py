from django.db import models

# Create your models here.
from django.forms import ModelForm

class UploadModel(models.Model):
   title = models.CharField(max_length=50)
   file = models.FileField(upload_to="uploads/%Y/%m/%d/", blank=True)

   def __unicode__(self):
       return unicode(self.title)

class DetectResModel(models.Model):
    parent_obj = models.IntegerField()
    file = models.FileField(blank=True)
