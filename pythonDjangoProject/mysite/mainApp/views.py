from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect
from django.conf import settings
from django.views.generic import TemplateView

from .forms import IdentifyForm, TestForm
from .models import TestModel

from uploadfileapp.views import clf, detectFunction

import subprocess # else  it will be --> NameError: name 'run_client' is not defined
import socket, pickle
from PIL import Image
import cv2, numpy, os, sys
import face_recognition

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
            res, de = run_client(fname, pk)

        args = {'form': form, 'f': f, 'res': res, 'de': de}
        return render(request, self.template_name, args)

def run_client(test_img, pk):
    detected = None
    answ = ""
    HOST = "127.0.0.1"
    PORT = 9999
    BUFFER_SIZE = 4096
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.connect((HOST, PORT))
        data_string = str.encode(test_img)
        sock.send(data_string)
        print('Send:', data_string)

        all_data = bytearray()
        while True:
            data = sock.recv(BUFFER_SIZE)
            if not data:
                break
            all_data += data

        obj = pickle.loads(all_data)
        detected = save_image(test_img, obj, pk)
    except Exception as e:
        answ = "something's wrong with %s:%d. Exception is %s" % (HOST, PORT, e)
    finally:
        sock.close()
    return answ, detected

def save_image(file, labels, pk):
    # Load the jpg file into a numpy array
    image = face_recognition.load_image_file(file)

    rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # Find all the faces in the image using the default HOG-based model.
    # This method is fairly accurate, but not as accurate as the CNN model and not GPU accelerated.
    # See also: find_faces_in_picture_cnn.py1111
    face_locations = face_recognition.face_locations(rgb_image)

    print("I found {} face(s) in this photograph.".format(len(face_locations)))
    for face_location in face_locations:
        # Print the location of each face in this image
        top, right, bottom, left = face_location
        print("A face is located at pixel location Top: {}, Left: {}, Bottom: {}, Right: {}".format(top, left, bottom, right))

    for (top, right, bottom, left), label in zip(face_locations, labels):
        x = int((right-left)/5)
        y = int((bottom-top)/5)
        # Draw a box around the face
        cv2.rectangle(rgb_image, (left-x, top-y), (right+x, bottom+y), (50,205,154), 3)
        # Draw a label with a name below the face
        cv2.rectangle(rgb_image, (left-x, bottom+int(y*2.2)), (right+x+3, bottom+y), (50,205,154), cv2.FILLED)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(rgb_image, label, (left-int(x*0.9), bottom+int(y*1.8)), font, 1.0, (0,0,0), 2)

    path = settings.BASE_DIR+"/media/tests/detected/"+pk
    print(path)
    if not os.path.exists(path): os.makedirs(path)
    f = "/imgRec.jpg"
    cv2.imwrite(path+"/"+f, rgb_image)

    rec = TestModel.objects.get(pk=pk)
    rec.detected = "tests/detected/"+pk+f
    rec.save()

    return "tests/detected/"+str(pk)+f
