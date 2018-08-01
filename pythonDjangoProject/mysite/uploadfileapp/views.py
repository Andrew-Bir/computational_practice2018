from django.shortcuts import render, redirect

# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect
from django.conf import settings
from django.views.generic import TemplateView

from .models import UploadModel, DetectResModel
from .forms import UploadForm, DetectForm

import subprocess # else  it will be --> NameError: name 'run_client' is not defined
import sys
from PIL import Image
import cv2, numpy
import time, datetime, os

# Create your views here.
def m_view(request):
    if request.method == 'POST':
        # Create a form instance from POST data.
        f = UploadForm(request.POST, request.FILES)
        if f.is_valid():
            f.save()
            return HttpResponseRedirect('/uploadfileapp/')
        return render(request, 'uploadfileapp/form_upload.html', {'form': f})
    else:
        f = UploadForm()
    return render(request, 'uploadfileapp/form_upload.html', {'form': f})

class DetectItem(TemplateView):
    template_name = "uploadfileapp/detect_form.html"

    def get(self, request, pk):
        obj = UploadModel.objects.get(pk=pk)
        title = obj.title
        file_name = obj.file.url

        form = DetectForm()
        args = {'form': form, 'title': title, 'file_name': file_name}
        return render(request, self.template_name, args)

    def post(self, request, pk):
        obj = UploadModel.objects.get(pk=pk)
        title = obj.title
        file_name = obj.file.url

        form = DetectForm(request.POST)
        if form.is_valid():
            t = time.strftime("%Y-%m-%d_%H:%M:%S")
            t_dir = settings.BASE_DIR + form.cleaned_data['path'] + pk + "/" + t
            fname = settings.BASE_DIR + file_name
            parent_obj = pk;
            dir = detect_and_crop(fname, t_dir, parent_obj, t)

        args = {'form': form, 'title': title, 'file_name': file_name, 'dir': dir}
        return render(request, self.template_name, args)


def detect_and_crop(image_path, target_dir, parent_obj, t):
    # Read the image
    image = cv2.imread(image_path)
    # for frontal faces
    face_cascade = clf("haarcascade_frontalface_default.xml")

    faces = detectFunction(image, face_cascade)
    msg = cropFunction(image, faces, target_dir, parent_obj, t)
    # Draw a rectangle around the faces
    '''for (x, y, w, h) in faces:
        cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), 2)
    cv2.imshow("Faces found", image)
    cv2.waitKey(2000)
    cv2.destroyAllWindows()'''
    return msg

def clf(fname):
    # Model parameters
    # modify this for your environment
    dir_path = settings.BASE_DIR + "/uploadfileapp/static/uploadfileapp/data/haarcascades"
    model_path = dir_path + "/" + fname
    # Create the classifier
    return cv2.CascadeClassifier(model_path)

def detectFunction(image, face_cascade):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    #Detect faces on image
    faces = face_cascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=8,
        minSize=(30, 30),
        flags=cv2.CASCADE_SCALE_IMAGE
    )
    print("Found {0} faces!".format(len(faces)))
    return faces

def cropFunction(image, faces, directory, parent_obj, t):
    i = 0
    #height, width = image.shape[:2]
    for (x, y, w, h) in faces:
        r = max(w, h) / 2
        centerx = x + w / 2
        centery = y + h / 2
        nx = int(centerx - r)
        ny = int(centery - r)
        nr = int(r * 2)

        faceimg = image[ny:ny+nr, nx:nx+nr]
        lastimg = cv2.resize(faceimg, (82, 82))
        i += 1
        # make dir and create face-files
        #directory = "result/"+time.strftime("%H-%M-%S")
        if not os.path.exists(directory):
            os.makedirs(directory)
        filename = directory + "/image" + str(i) + ".jpg"
        cv2.imwrite(filename, lastimg)

        # Create a new record using the model's constructor.
        a_record = DetectResModel(parent_obj=parent_obj)
        # model FileField
        a_record.file = "results/"+parent_obj+"/"+t+"/image" + str(i) + ".jpg"
        # Save the object into the database.
        a_record.save(force_insert=True)

    return directory
