# face_identify.py

import face_recognition
import numpy as np
import cv2 as cv

from arrays import face_names, known_faces

def identify(test_img):
    # Load the jpg files into numpy arrays
    unknown_image = face_recognition.load_image_file(test_img)
    try:
        # --------------------------------------------------------------------------
        # Get the face encodings for each face in each image file:
        # list_of_face_encodings = face_recognition.face_encodings(image)
        # it returns a list of encodings.
        # But since I know each image only has one face, I only care about the first encoding in each image,
        # so I take index 0.
        # --------------------------------------------------------------------------
        unknown_face_encoding = face_recognition.face_encodings(unknown_image)[0]
        # --------------------------------------------------------------------------
        # Finding the encoding for a face is a bit slow,
        # so you might want to save the results for each image in a database or cache
        # if you need to refer back to it later.
        # --------------------------------------------------------------------------
    except IndexError:
        print("I wasn't able to locate any faces in at least one of the images. Check the image files. Aborting...")
        quit()

    # results is an array of True/False telling if the unknown face matched anyone in the known_faces array
    results = face_recognition.compare_faces(known_faces, unknown_face_encoding)

    if not True in results:
        return "The unknown face is new person that we've never seen before"
    else:
        for res, name in zip(results, face_names):
            if res:
                return name

if __name__ == "__main__":
    #img = "test_data/test1.jpg"
    identify(img)
