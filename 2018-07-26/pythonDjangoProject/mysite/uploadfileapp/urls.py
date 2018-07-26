from django.conf.urls import url, include
from django.views.generic import ListView, DetailView

from .models import UploadModel, DetectResModel
from . import views
from .views import DetectItem

urlpatterns = [
    url(r'^$', ListView.as_view(queryset=UploadModel.objects.all().order_by("title"), template_name="uploadfileapp/mainPage.html")),
    url(r'^uploadFile/$', views.m_view, name='m_view'),
    url(r'^(?P<pk>\d+)$', DetailView.as_view(model=UploadModel, template_name="uploadfileapp/file.html")),
    url(r'^detect/(?P<pk>\d+)$', DetectItem.as_view(), name='detect'),
    url(r'^results/$', ListView.as_view(queryset=DetectResModel.objects.all().order_by("parent_obj"), template_name="uploadfileapp/results.html")),
]
