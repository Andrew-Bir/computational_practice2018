from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect
from django.conf import settings
from django.views.generic import TemplateView

from .forms import IdentifyForm, TestForm
from .models import TestModel

import subprocess # else  it will be --> NameError: name 'run_client' is not defined
import socket
from PIL import Image
import cv2, numpy, os

# Create your views here.
def test_view(request):
    if request.method == 'POST':
        # Create a form instance from POST data.
        f = TestForm(request.POST, request.FILES)
        if f.is_valid():
            f.save()
            return HttpResponseRedirect('/')
        return render(request, 'mainApp/addfaceForm.html', {'form': f})
    else:
        f = TestForm()
    return render(request, 'mainApp/addfaceForm.html', {'form': f})


class Identify(TemplateView):
    template_name = "mainApp/unknownFace.html"

    def get(self, request, pk):
        obj = TestModel.objects.get(pk=pk)
        f = obj.file.url

        form = IdentifyForm()
        args = {'form': form, 'f': f}
        return render(request, self.template_name, args)

    def post(self, request, pk):
        obj = TestModel.objects.get(pk=pk)
        f = obj.file.url

        form = IdentifyForm(request.POST)
        if form.is_valid():
            fname = settings.BASE_DIR + f
            res = run_client(fname)

        args = {'form': form, 'f': f, 'res': res}
        return render(request, self.template_name, args)

def run_client(fname):
    HOST = "127.0.0.1"
    PORT = 9999
    conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        conn.connect((HOST, PORT))

        tmp = str.encode(fname)
        conn.send(tmp)
        data = conn.recv(2048)
        answ = data.decode()
    except Exception as e:
        answ = "something's wrong with %s:%d. Exception is %s" % (HOST, PORT, e)
    finally:
        conn.close()

    return answ
