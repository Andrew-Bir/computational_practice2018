from django.contrib import admin

# Register your models here.
from .models import UploadModel, DetectResModel
admin.site.register(UploadModel)
admin.site.register(DetectResModel)
