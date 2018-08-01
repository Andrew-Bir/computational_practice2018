from django.conf.urls import url, include
from django.views.generic import ListView, DetailView
from . import views
from .views import Identify
from .models import TestModel

urlpatterns = [
    #url(r'^$', views.index, name='index'),
    url(r'^$', ListView.as_view(queryset=TestModel.objects.all().order_by("id"), template_name="mainApp/mainPage.html")),
    url(r'^uploadTest/$', views.test_view, name='test_view'),
    url(r'^identify/(?P<pk>\d+)$', Identify.as_view(), name='identify'),
]
